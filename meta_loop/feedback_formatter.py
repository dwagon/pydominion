"""Format tournament results as text for the LLM."""

from __future__ import annotations

import re

from tournament.results import TournamentResult, MatchupResult

# Max characters for all traces combined in the feedback.
# ~15K chars ≈ ~4K tokens — leaves room for stats + the rest of the prompt.
MAX_TRACE_CHARS = 15000


def _clean_spectator_log(log: str) -> str:
    """Strip verbose state-dump blocks from the spectator log.

    The engine emits blocks like:
        Name: --------------------------------------------------
        Name: | Phase: Buy
        Name: | Hand (5): Copper, Copper, ...
        Name: --------------------------------------------------

    These are redundant noise for the LLM. Strip them and keep the
    action lines (Bought X, Played X, Trashed X, etc.) and turn headers.
    """
    cleaned_lines: list[str] = []
    in_state_block = False

    for line in log.splitlines():
        # Detect start/end of state dump blocks
        if re.search(r"-{20,}", line):
            in_state_block = not in_state_block
            continue

        if in_state_block:
            continue

        # Skip empty/whitespace-only lines
        stripped = line.strip()
        if not stripped:
            continue

        # Skip redundant "Have N coins" lines
        if re.search(r"Have \d+ coins$", stripped):
            continue

        # Skip lines that are just the player name with nothing else
        if re.match(r"^\w+:\s*$", stripped):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def format_feedback(
    result: TournamentResult,
    agent_name: str,
    iteration: int,
) -> str:
    """Build a structured feedback string from tournament results.

    Includes: rating table, head-to-head stats, and sample game traces.
    Traces are drawn from the weakest matchup for the agent.
    Traces are cleaned (state dumps stripped) and capped at MAX_TRACE_CHARS.
    """
    lines: list[str] = [f"== Tournament Results (Iteration {iteration}) ==", ""]

    # --- Ratings table ---
    lines.append("Ratings (TrueSkill mu ± sigma):")
    sorted_ratings = sorted(
        result.ratings_detail.items(), key=lambda x: -x[1].rating
    )
    for name, detail in sorted_ratings:
        marker = " <-- you" if name == agent_name else ""
        lines.append(
            f"  {name:20s}  {detail.rating:6.1f} ± {detail.uncertainty:.1f}  "
            f"(win rate: {detail.win_rate:.1%}){marker}"
        )
    lines.append("")

    # --- Head-to-head details for agent vs each opponent ---
    for (p1, p2), matchup in result.matchups.items():
        if agent_name not in (p1, p2):
            continue

        opponent = p2 if p1 == agent_name else p1

        if p1 == agent_name:
            wins, losses = matchup.wins_a, matchup.wins_b
            wr = matchup.win_rate_a
            avg_vp, opp_vp = matchup.avg_vp_a, matchup.avg_vp_b
        else:
            wins, losses = matchup.wins_b, matchup.wins_a
            wr = 1.0 - matchup.win_rate_a
            avg_vp, opp_vp = matchup.avg_vp_b, matchup.avg_vp_a

        lines.append(f"Head-to-head vs {opponent}:")
        lines.append(
            f"  Record: {wins}-{losses}-{matchup.draws} "
            f"({wr:.1%} win rate)"
        )
        lines.append(
            f"  Avg VP: {avg_vp:.1f} vs {opp_vp:.1f} "
            f"(margin: {avg_vp - opp_vp:+.1f})"
        )
        lines.append(f"  Avg game length: {matchup.avg_game_length:.1f} turns")
        lines.append("")

    lines.append(
        f"{result.total_games} games played in {result.wall_seconds:.1f}s "
        f"({result.games_per_second:.0f} games/sec)"
    )
    lines.append("")

    # --- Game traces ---
    # Show traces from the weakest matchup (most useful for learning).
    traces_shown = 0
    max_traces = 3
    trace_chars_used = 0

    # Collect all matchups involving the agent, sorted by agent win rate (ascending)
    agent_matchups = []
    for (p1, p2), matchup in result.matchups.items():
        if agent_name not in (p1, p2):
            continue
        if p1 == agent_name:
            wr = matchup.win_rate_a
        else:
            wr = 1.0 - matchup.win_rate_a
        agent_matchups.append(((p1, p2), matchup, wr))

    agent_matchups.sort(key=lambda x: x[2])  # worst matchup first

    if agent_matchups:
        lines.append("== Sample Game Traces (from weakest matchups) ==")
        lines.append("")

        for (p1, p2), matchup, wr in agent_matchups:
            if traces_shown >= max_traces:
                break
            if not matchup.traces:
                continue

            opponent = p2 if p1 == agent_name else p1

            for trace in matchup.traces:
                if traces_shown >= max_traces:
                    break
                if trace_chars_used >= MAX_TRACE_CHARS:
                    lines.append("(remaining traces omitted — character limit reached)")
                    traces_shown = max_traces  # stop
                    break

                agent_score = trace.final_scores.get(agent_name, 0)
                opp_score = 0
                for pname, sc in trace.final_scores.items():
                    if pname != agent_name:
                        opp_score = sc

                # Determine outcome label
                if trace.outcome == "win_a":
                    label = "WON" if p1 == agent_name else "LOST"
                elif trace.outcome == "win_b":
                    label = "LOST" if p1 == agent_name else "WON"
                else:
                    label = "DRAW"

                header = (
                    f"--- Game #{trace.game_number}: "
                    f"{label} ({agent_score} vs {opp_score} VP, "
                    f"{trace.num_turns} turns) vs {opponent} ---"
                )
                lines.append(header)

                if trace.spectator_log:
                    cleaned = _clean_spectator_log(trace.spectator_log)
                    # Truncate if it would blow the budget
                    budget_remaining = MAX_TRACE_CHARS - trace_chars_used
                    if len(cleaned) > budget_remaining:
                        cleaned = cleaned[:budget_remaining] + "\n... (trace truncated)"
                    lines.append(cleaned)
                    trace_chars_used += len(cleaned)
                else:
                    lines.append("(trace not available)")

                lines.append("")
                traces_shown += 1

    return "\n".join(lines)

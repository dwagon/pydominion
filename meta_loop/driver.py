"""Single-shot heuristic evaluation driver.

LLM reads kingdom card text → writes heuristic player → tournament evaluates.
"""

from __future__ import annotations

import os
import random
import time
from typing import Optional

from rich.console import Console

from dominion.BotPlayer import BotPlayer
from dominion.NaiveBotPlayer import NaiveBotPlayer
from tournament import run_agent_matchups

from .code_extractor import count_lines, extract_code, validate_and_load
from .kingdom_builder import get_kingdom_description, get_resolved_mechanics
from .llm_client import LLMClient, LLMResponse
from .logger import RunLogger
from .prompts import SYSTEM_PROMPT, build_fix_prompt, build_initial_prompt
from .results import EvalResult

console = Console()

# Number of fix attempts when validation fails
MAX_FIX_ATTEMPTS = 3

# Rough cost per million tokens (USD) for common models.
# Used for estimation only — not billing.
MODEL_COSTS: dict[str, tuple[float, float]] = {
    # (prompt_cost_per_mtok, completion_cost_per_mtok)
    "anthropic/claude-sonnet-4-20250514": (3.0, 15.0),
    "anthropic/claude-opus-4-20250514": (15.0, 75.0),
    "anthropic/claude-haiku-3-20240307": (0.25, 1.25),
    "anthropic/claude-3.5-sonnet": (3.0, 15.0),
    "openai/gpt-4o": (2.5, 10.0),
    "openai/gpt-4o-mini": (0.15, 0.6),
    "google/gemini-2.0-flash-001": (0.1, 0.4),
    "google/gemini-3-flash-preview": (0.1, 0.4),
    "deepseek/deepseek-chat-v3-0324": (0.27, 1.10),
    "deepseek/deepseek-r1": (0.55, 2.19),
}

DEFAULT_COST = (1.0, 3.0)


def _estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Estimate USD cost from token counts."""
    prompt_rate, completion_rate = MODEL_COSTS.get(model, DEFAULT_COST)
    return (prompt_tokens * prompt_rate + completion_tokens * completion_rate) / 1_000_000


def run_eval(
    kingdom_cards: list[str],
    games_per_eval: int = 200,
    llm_backend: str = "openrouter",
    model: str = "anthropic/claude-sonnet-4-20250514",
    seed: Optional[int] = None,
    output_dir: str = "runs/default",
    temperature: float = 0.3,
    max_tokens: int = 8192,
    game_kwargs: Optional[dict] = None,
) -> EvalResult:
    """Single-shot: LLM writes heuristic → tournament evaluates it.

    ``game_kwargs`` are forwarded to the Dominion Game constructor and
    kingdom description builder.  Use this to enable prosperity
    (``prosperity=True``), events, landmarks, etc.
    """
    if game_kwargs is None:
        game_kwargs = {}

    if seed is None:
        seed = random.randint(0, 2**31 - 1)

    run_start = time.monotonic()

    # --- Setup ---
    llm = LLMClient(backend=llm_backend, model=model)
    logger = RunLogger(output_dir, kingdom_cards, model)
    resolved = get_resolved_mechanics(kingdom_cards, **game_kwargs)
    logger.write_config(
        games_per_eval=games_per_eval,
        seed=seed,
        temperature=temperature,
        game_kwargs=game_kwargs if game_kwargs else {},
        resolved_mechanics=resolved if resolved else {},
    )

    kingdom_desc = get_kingdom_description(kingdom_cards, **game_kwargs)
    logger.write_kingdom_description(kingdom_desc)

    console.print(f"\n[bold cyan]Single-Shot Eval[/]")
    console.print(f"  Kingdom: {', '.join(kingdom_cards)}")
    console.print(f"  Model: {model}")
    console.print(f"  Games per matchup: {games_per_eval} (×2 for side swap)")
    console.print(f"  Output: {output_dir}")
    console.print()

    # --- Step 1: Build prompt ---
    user_prompt = build_initial_prompt(kingdom_desc)
    logger.write_prompt(1, SYSTEM_PROMPT, user_prompt)

    # --- Step 2: Call LLM ---
    console.print("  [dim]Calling LLM...[/]", end=" ")
    llm_resp = _call_llm_with_retry(
        llm, SYSTEM_PROMPT, user_prompt,
        temperature=temperature, max_tokens=max_tokens,
    )
    cost = _estimate_cost(model, llm_resp.prompt_tokens, llm_resp.completion_tokens)
    console.print(
        f"[green]{llm_resp.completion_tokens} tokens, "
        f"{llm_resp.latency_seconds:.1f}s, ~${cost:.4f}[/]"
    )
    logger.write_llm_response(1, llm_resp.text)
    logger.write_llm_reasoning(1, llm_resp.reasoning)

    # --- Step 3: Extract and validate ---
    console.print("  [dim]Validating heuristic...[/]", end=" ")
    code, cls, validation_errors, validation_attempts = _extract_and_validate(
        llm, llm_resp.text, kingdom_cards, logger,
        temperature=temperature, max_tokens=max_tokens,
    )

    if cls is None:
        console.print("[red]FAILED — could not produce valid heuristic[/]")
        logger.write_validation_errors(1, validation_errors)
        total_wall = time.monotonic() - run_start
        result = EvalResult(
            kingdom=kingdom_cards, model=model,
            vs_bigmoney_win_rate=0.0, vs_bigmoney_avg_vp_margin=0.0,
            vs_all_win_rates={}, trueskill_mu=0.0, trueskill_sigma=0.0,
            total_games=0, eval_seconds=0.0,
            llm_prompt_tokens=llm_resp.prompt_tokens,
            llm_completion_tokens=llm_resp.completion_tokens,
            llm_latency_seconds=llm_resp.latency_seconds,
            validation_attempts=validation_attempts,
            heuristic_loc=0, estimated_cost_usd=cost,
            total_wall_time_seconds=total_wall,
            output_dir=output_dir, success=False,
        )
        logger.write_summary(result)
        return result

    console.print(f"[green]OK ({count_lines(code)} LOC, {validation_attempts} attempt(s))[/]")
    logger.write_validation_errors(1, validation_errors)
    logger.write_heuristic(1, code)

    # --- Step 4: Evaluate ---
    agent_name = "agent"
    opponents: dict[str, type] = {
        "bigmoney": BotPlayer,
        "naive": NaiveBotPlayer,
    }
    console.print(
        f"  [dim]Running evaluation ({len(opponents)} opponents, "
        f"{games_per_eval}×2 games each)...[/]",
        end=" ",
    )
    tournament_result = run_agent_matchups(
        agent_name=agent_name,
        agent_class=cls,
        opponents=opponents,
        kingdom_cards=kingdom_cards,
        num_games_per_matchup=games_per_eval,
        seed=seed,
        collect_traces=0,
        **game_kwargs,
    )
    console.print(
        f"[green]{tournament_result.total_games} games in "
        f"{tournament_result.wall_seconds:.1f}s[/]"
    )
    logger.write_tournament_result(1, tournament_result)

    # --- Step 5: Extract metrics ---
    vs_bm_wr = _get_win_rate(tournament_result, agent_name, "bigmoney")
    vs_bm_margin = _get_vp_margin(tournament_result, agent_name, "bigmoney")

    vs_all: dict[str, float] = {}
    for opp_name in opponents:
        vs_all[opp_name] = _get_win_rate(tournament_result, agent_name, opp_name)

    # Collect per-opponent crash counts from matchup results
    crashes_by_opp: dict[str, int] = {}
    for (p1, p2), matchup in tournament_result.matchups.items():
        if p1 == agent_name:
            crashes_by_opp[p2] = matchup.crashes
        elif p2 == agent_name:
            crashes_by_opp[p1] = matchup.crashes
    total_crashes = sum(crashes_by_opp.values())

    # Compute avg game length across all matchups (weighted by num_games)
    total_matchup_games = sum(m.num_games for m in tournament_result.matchups.values())
    avg_game_length = (
        sum(m.avg_game_length * m.num_games for m in tournament_result.matchups.values())
        / total_matchup_games
        if total_matchup_games > 0 else 0.0
    )

    detail = tournament_result.ratings_detail.get(agent_name)
    mu = detail.rating if detail else 0.0
    sigma = detail.uncertainty if detail else 0.0

    total_wall = time.monotonic() - run_start

    result = EvalResult(
        kingdom=kingdom_cards,
        model=model,
        vs_bigmoney_win_rate=vs_bm_wr,
        vs_bigmoney_avg_vp_margin=vs_bm_margin,
        vs_all_win_rates=vs_all,
        trueskill_mu=mu,
        trueskill_sigma=sigma,
        total_games=tournament_result.total_games,
        eval_seconds=tournament_result.wall_seconds,
        llm_prompt_tokens=llm_resp.prompt_tokens,
        llm_completion_tokens=llm_resp.completion_tokens,
        llm_latency_seconds=llm_resp.latency_seconds,
        validation_attempts=validation_attempts,
        heuristic_loc=count_lines(code),
        estimated_cost_usd=cost,
        total_wall_time_seconds=total_wall,
        output_dir=output_dir,
        success=True,
        avg_game_length=avg_game_length,
        crashes_by_opponent=crashes_by_opp if crashes_by_opp else None,
    )
    logger.write_summary(result)

    # Save heuristic at top level
    best_path = os.path.join(output_dir, "best_heuristic.py")
    with open(best_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Print summary
    crash_str = f"  [red]crashes={total_crashes}/{tournament_result.total_games}[/]" if total_crashes else ""
    console.print(
        f"  [bold]vs BigMoney: {vs_bm_wr:.1%}[/]  "
        f"margin={vs_bm_margin:+.1f}  mu={mu:.1f}"
        + (f"  [red]crashes={total_crashes}[/]" if total_crashes else "")
    )
    for opp, wr in vs_all.items():
        if opp != "bigmoney":
            opp_crashes = crashes_by_opp.get(opp, 0)
            crash_note = f" [red]({opp_crashes} crashes)[/]" if opp_crashes else ""
            console.print(f"  [dim]vs {opp}: {wr:.0%}[/]{crash_note}")
    console.print()

    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _call_llm_with_retry(
    llm: LLMClient,
    system: str,
    user: str,
    temperature: float = 0.3,
    max_tokens: int = 8192,
    retries: int = 3,
) -> LLMResponse:
    """Call the LLM with exponential backoff on transient errors."""
    import time as _time

    for attempt in range(retries):
        try:
            return llm.complete(system, user, max_tokens=max_tokens,
                                temperature=temperature)
        except Exception as e:
            if attempt == retries - 1:
                raise
            wait = 2 ** (attempt + 1)
            console.print(f"  [yellow]LLM error: {e}. Retrying in {wait}s...[/]")
            _time.sleep(wait)
    raise RuntimeError("LLM retry loop exited unexpectedly")


def _extract_and_validate(
    llm: LLMClient,
    initial_response: str,
    kingdom_cards: list[str],
    logger: RunLogger,
    temperature: float = 0.3,
    max_tokens: int = 8192,
) -> tuple[Optional[str], Optional[type], list[str], int]:
    """Extract code, validate, and retry with fix prompts on failure.

    Returns (code, cls, validation_errors, attempt_count).
    code/cls are None if all attempts failed.
    """
    errors: list[str] = []
    response_text = initial_response

    for attempt in range(1, MAX_FIX_ATTEMPTS + 1):
        try:
            code = extract_code(response_text)
        except ValueError as e:
            error_msg = f"Attempt {attempt}: {e}"
            errors.append(error_msg)
            if attempt < MAX_FIX_ATTEMPTS:
                console.print(f"[yellow]no code block, asking for fix...[/]", end=" ")
                fix_prompt = build_fix_prompt("(no code extracted)", str(e))
                fix_resp = _call_llm_with_retry(llm, SYSTEM_PROMPT, fix_prompt,
                                                 temperature=temperature, max_tokens=max_tokens)
                logger.write_llm_response(1, f"--- Fix attempt {attempt} ---\n{fix_resp.text}")
                response_text = fix_resp.text
            continue

        try:
            cls = validate_and_load(code, kingdom_cards)
            return code, cls, errors, attempt
        except ValueError as e:
            error_msg = f"Attempt {attempt}: {e}"
            errors.append(error_msg)
            if attempt < MAX_FIX_ATTEMPTS:
                console.print(f"[yellow]validation failed, asking for fix...[/]", end=" ")
                fix_prompt = build_fix_prompt(code, str(e))
                fix_resp = _call_llm_with_retry(llm, SYSTEM_PROMPT, fix_prompt,
                                                 temperature=temperature, max_tokens=max_tokens)
                logger.write_llm_response(1, f"--- Fix attempt {attempt} ---\n{fix_resp.text}")
                response_text = fix_resp.text

    return None, None, errors, MAX_FIX_ATTEMPTS


def _get_win_rate(result, agent_name: str, opponent_name: str) -> float:
    for (p1, p2), matchup in result.matchups.items():
        if p1 == agent_name and p2 == opponent_name:
            return matchup.win_rate_a
        if p1 == opponent_name and p2 == agent_name:
            return 1.0 - matchup.win_rate_a
    return 0.0


def _get_vp_margin(result, agent_name: str, opponent_name: str) -> float:
    for (p1, p2), matchup in result.matchups.items():
        if p1 == agent_name and p2 == opponent_name:
            return matchup.avg_vp_margin
        if p1 == opponent_name and p2 == agent_name:
            return -matchup.avg_vp_margin
    return 0.0

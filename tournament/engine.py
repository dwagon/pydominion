import logging
import time
import io
import sys
import random
from typing import Optional, Any
from copy import deepcopy

from dominion.Game import Game
from .results import TournamentResult, MatchupResult, GameTrace
from .ratings import TournamentRatings
from .trace_collector import TraceCollector

logger = logging.getLogger(__name__)

def _run_single_game(
    kingdom_cards: list[str],
    player_classes: list[type],
    seed: int,
    **game_kwargs: Any,
) -> tuple[str, dict[str, int], int]:
    """Runs a single fast game and returns (outcome, scores, turns)"""
    random.seed(seed)

    # Standard Game setup
    game = Game(
        initcards=kingdom_cards,
        numplayers=2,
        quiet=True,
        player_classes=player_classes,
        **game_kwargs,
    )
    game.start_game()
    
    # Run until over or max turns
    while not game.game_over and len(game._turns) < 400:
        game.turn()

    # Determine winner
    scores = {}
    for p in game.player_list():
        scores[p.name] = p.get_score()

    p1_name = game.player_list()[0].name
    p2_name = game.player_list()[1].name

    p1_score = scores[p1_name]
    p2_score = scores[p2_name]

    if p1_score > p2_score:
        outcome = "win_a"
    elif p2_score > p1_score:
        outcome = "win_b"
    else:
        outcome = "draw"

    return outcome, scores, max(p.turn_number for p in game.player_list())

def _run_traced_game(
    kingdom_cards: list[str],
    player_classes: list[type],
    seed: int,
    **game_kwargs: Any,
) -> str:
    """Re-run a game with the given seed and capture a structured log."""
    random.seed(seed)
    game = Game(initcards=kingdom_cards, numplayers=2, quiet=True,
                player_classes=player_classes, **game_kwargs)
    game.start_game()

    # Shared log buffer
    log_lines = []

    # Monkey-patch output on all players and the game
    def make_player_output(player, log):
        def patched_output(msg, end="\n"):
            log.append(f"{player.name}: {msg}")
            # Ensure the message is still appended to the player's internal list
            # in case any other part of the game relies on it before it gets cleared
            if not hasattr(player, 'messages'):
                player.messages = []
            player.messages.append(msg)
        return patched_output

    def make_game_output(log):
        def patched_output(msg):
            log.append(f"ALL: {msg}")
        return patched_output

    for p in game.player_list():
        p.output = make_player_output(p, log_lines)
    game.output = make_game_output(log_lines)

    while not game.game_over and len(game._turns) < 400:
        game.turn()

    # Final scores
    for p in game.player_list():
        score = p.get_score()
        cards = p.get_cards()
        deck_str = ', '.join(f"{k}={v}" for k, v in sorted(cards.items()))
        log_lines.append(f"FINAL: {p.name}: {score} VP  [{deck_str}]")

    return '\n'.join(log_lines)

def _run_matchup(
    p1_name: str,
    p1_class: type,
    p2_name: str,
    p2_class: type,
    kingdom_cards: list[str],
    num_games_per_matchup: int,
    start_total_games: int,
    seed: int,
    collect_traces: int,
    ratings: TournamentRatings,
    **game_kwargs: Any,
) -> tuple[MatchupResult, int, int]:
    """Runs a single matchup between two bots (p1 goes first, then p2 goes first)."""
    p1_wins = 0
    p2_wins = 0
    draws = 0
    p1_vp_total = 0
    p2_vp_total = 0
    turns_total = 0

    trace_collector = TraceCollector(p1_name, p2_name, collect_traces)
    crashes = 0
    total_games = start_total_games

    # P1 goes first
    for g in range(num_games_per_matchup):
        game_num = total_games + 1
        game_seed = seed + game_num

        try:
            outcome, scores, turns = _run_single_game(
                kingdom_cards=kingdom_cards,
                player_classes=[p1_class, p2_class],
                seed=game_seed,
                **game_kwargs,
            )
            p1_actual = list(scores.keys())[0]
            p2_actual = list(scores.keys())[1]
            p1_score = scores[p1_actual]
            p2_score = scores[p2_actual]
        except Exception as e:
            crashes += 1
            if crashes <= 3:
                logger.warning("Agent crashed in game %d: %s", game_num, e)
            outcome = "win_b"
            p1_score, p2_score = 0, 6
            turns = 0

        if outcome == "win_a":
            p1_wins += 1
        elif outcome == "win_b":
            p2_wins += 1
        else:
            draws += 1

        p1_vp_total += p1_score
        p2_vp_total += p2_score
        turns_total += turns
        total_games += 1

        trace = GameTrace(
            game_number=game_num,
            player_a=p1_name,
            player_b=p2_name,
            outcome=outcome,
            final_scores={p1_name: p1_score, p2_name: p2_score},
            num_turns=turns,
            kingdom_cards=kingdom_cards,
            seed=game_seed,
            spectator_log="",
        )
        trace_collector.add_trace(trace, p1_score - p2_score)
        ratings.add_game(p1_name, p2_name, outcome)

    # P2 goes first
    first_half_total = total_games
    for g in range(num_games_per_matchup):
        game_num = total_games + 1
        game_seed = seed + game_num

        try:
            outcome, scores, turns = _run_single_game(
                kingdom_cards=kingdom_cards,
                player_classes=[p2_class, p1_class],
                seed=game_seed,
                **game_kwargs,
            )
            p2_actual = list(scores.keys())[0]
            p1_actual = list(scores.keys())[1]
            p2_score = scores[p2_actual]
            p1_score = scores[p1_actual]

            if outcome == "win_a":
                p2_wins += 1
                mapped_outcome = "win_b"
            elif outcome == "win_b":
                p1_wins += 1
                mapped_outcome = "win_a"
            else:
                draws += 1
                mapped_outcome = "draw"
        except Exception as e:
            crashes += 1
            if crashes <= 3:
                logger.warning("Agent crashed in game %d: %s", game_num, e)
            mapped_outcome = "win_b"
            p2_wins += 1
            p1_score, p2_score = 0, 6
            turns = 0

        p1_vp_total += p1_score
        p2_vp_total += p2_score
        turns_total += turns
        total_games += 1

        trace = GameTrace(
            game_number=game_num,
            player_a=p1_name,
            player_b=p2_name,
            outcome=mapped_outcome,
            final_scores={p1_name: p1_score, p2_name: p2_score},
            num_turns=turns,
            kingdom_cards=kingdom_cards,
            seed=game_seed,
            spectator_log="",
        )
        trace_collector.add_trace(trace, p1_score - p2_score)
        ratings.add_game(p1_name, p2_name, mapped_outcome)

    if crashes:
        logger.warning(
            "Agent crashed in %d/%d games vs %s",
            crashes, num_games_per_matchup * 2, p2_name,
        )

    total_matchup_games = num_games_per_matchup * 2

    # Collect traces for selected games
    sampled_traces = trace_collector.get_sampled_traces()
    for trace in sampled_traces:
        is_p1_first = trace.game_number <= first_half_total
        classes = [p1_class, p2_class] if is_p1_first else [p2_class, p1_class]
        trace.spectator_log = _run_traced_game(
            kingdom_cards=kingdom_cards,
            player_classes=classes,
            seed=trace.seed,
            **game_kwargs,
        )

    matchup_result = MatchupResult(
        player_a=p1_name,
        player_b=p2_name,
        wins_a=p1_wins,
        wins_b=p2_wins,
        draws=draws,
        num_games=total_matchup_games,
        win_rate_a=p1_wins / total_matchup_games,
        avg_vp_a=p1_vp_total / total_matchup_games,
        avg_vp_b=p2_vp_total / total_matchup_games,
        avg_vp_margin=(p1_vp_total - p2_vp_total) / total_matchup_games,
        avg_game_length=turns_total / total_matchup_games,
        crashes=crashes,
        traces=sampled_traces,
    )

    return matchup_result, total_games, crashes


def run_agent_matchups(
    agent_name: str,
    agent_class: type,
    opponents: dict[str, type],
    kingdom_cards: list[str],
    num_games_per_matchup: int = 200,
    seed: Optional[int] = None,
    collect_traces: int = 5,
    **game_kwargs: Any,
) -> TournamentResult:
    """Run one focal agent against each opponent (no opponent-vs-opponent games).

    This is the preferred evaluation function for the meta-loop: for iteration N,
    only the current heuristic needs to be tested.  Previous matchups are already
    recorded in earlier iterations.

    Extra ``**game_kwargs`` are forwarded to the ``Game`` constructor for every
    game (e.g. ``prosperity=True``, ``events=[...]``).

    Returns a TournamentResult with the same shape as run_tournament(), but only
    containing matchups that involve *agent_name*.
    """
    if seed is None:
        seed = random.randint(0, 2**31 - 1)

    start_time = time.time()
    ratings = TournamentRatings()
    matchups = {}
    total_games = 0

    for opp_name, opp_class in opponents.items():
        matchup_result, total_games, _ = _run_matchup(
            p1_name=agent_name,
            p1_class=agent_class,
            p2_name=opp_name,
            p2_class=opp_class,
            kingdom_cards=kingdom_cards,
            num_games_per_matchup=num_games_per_matchup,
            start_total_games=total_games,
            seed=seed,
            collect_traces=collect_traces,
            ratings=ratings,
            **game_kwargs,
        )
        matchups[(agent_name, opp_name)] = matchup_result

    end_time = time.time()
    wall_seconds = end_time - start_time

    return TournamentResult(
        ratings=ratings.get_ratings_dict(),
        ratings_detail=ratings.get_details(),
        matchups=matchups,
        total_games=total_games,
        wall_seconds=wall_seconds,
        games_per_second=total_games / wall_seconds if wall_seconds > 0 else 0,
    )


def run_tournament(
    players: dict[str, type],
    kingdom_cards: list[str],
    num_games_per_matchup: int = 200,
    seed: Optional[int] = None,
    collect_traces: int = 5,
    **game_kwargs: Any,
) -> TournamentResult:
    """Runs a round-robin tournament."""
    if seed is None:
        seed = random.randint(0, 2**31 - 1)
        
    start_time = time.time()
    ratings = TournamentRatings()
    matchups = {}
    total_games = 0
    
    player_names = list(players.keys())
    
    for i in range(len(player_names)):
        for j in range(i + 1, len(player_names)):
            p1_name = player_names[i]
            p2_name = player_names[j]
            p1_class = players[p1_name]
            p2_class = players[p2_name]
            
            matchup_result, total_games, _ = _run_matchup(
                p1_name=p1_name,
                p1_class=p1_class,
                p2_name=p2_name,
                p2_class=p2_class,
                kingdom_cards=kingdom_cards,
                num_games_per_matchup=num_games_per_matchup,
                start_total_games=total_games,
                seed=seed,
                collect_traces=collect_traces,
                ratings=ratings,
                **game_kwargs,
            )
            matchups[(p1_name, p2_name)] = matchup_result
            
    end_time = time.time()
    wall_seconds = end_time - start_time
    
    return TournamentResult(
        ratings=ratings.get_ratings_dict(),
        ratings_detail=ratings.get_details(),
        matchups=matchups,
        total_games=total_games,
        wall_seconds=wall_seconds,
        games_per_second=total_games / wall_seconds if wall_seconds > 0 else 0
    )

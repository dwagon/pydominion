#!/usr/bin/env python3
"""Round-robin tournament across all BotPlayer duchy × province strategy combinations.

Usage:
    uv run python bm_tournament.py
    uv run python bm_tournament.py --games 500
    uv run python bm_tournament.py --kingdom Chapel Village Smithy Market Militia
    uv run python bm_tournament.py --seed 42
    uv run python bm_tournament.py --duchy-only    # skip province axis
    uv run python bm_tournament.py --province-only # skip duchy axis
"""

from __future__ import annotations

import argparse
import functools
from typing import Any

from rich.console import Console
from rich.table import Table
from rich import box

from dominion.BotPlayer import BotPlayer, DuchyStrategy, ProvinceStrategy
from tournament.engine import run_tournament
from tournament.results import TournamentResult

console = Console(width=120)

DEFAULT_KINGDOM = [
    "Chapel", "Village", "Smithy", "Market", "Militia",
    "Moat", "Festival", "Laboratory", "Workshop", "Witch",
]

DUCHY_STRATEGIES: dict[str, DuchyStrategy] = {
    "dGreedy":    DuchyStrategy.GREEDY,
    "d5Prov":     DuchyStrategy.FIVE_PROVINCE,
    "dNone":      DuchyStrategy.NO_DUCHY,
}

PROVINCE_STRATEGIES: dict[str, ProvinceStrategy] = {
    "pGreedy": ProvinceStrategy.GREEDY,
    "pT12":    ProvinceStrategy.TURN_12,
}


def make_player_class(duchy: DuchyStrategy, province: ProvinceStrategy) -> type:
    """Return a BotPlayer partial pre-bound with both strategy kwargs."""
    return functools.partial(  # type: ignore[return-value]
        BotPlayer,
        duchy_strategy=duchy,
        province_strategy=province,
    )


def build_players(duchy_only: bool, province_only: bool) -> dict[str, type]:
    """Build the dict of player name → class for every active strategy combination."""
    players: dict[str, type] = {}

    if duchy_only:
        # Fix province at GREEDY, vary duchy
        for d_name, d_strat in DUCHY_STRATEGIES.items():
            players[d_name] = make_player_class(d_strat, ProvinceStrategy.GREEDY)
    elif province_only:
        # Fix duchy at GREEDY, vary province
        for p_name, p_strat in PROVINCE_STRATEGIES.items():
            players[p_name] = make_player_class(DuchyStrategy.GREEDY, p_strat)
    else:
        # Full 3×2 cross product
        for d_name, d_strat in DUCHY_STRATEGIES.items():
            for p_name, p_strat in PROVINCE_STRATEGIES.items():
                label = f"{d_name} {p_name}"
                players[label] = make_player_class(d_strat, p_strat)

    return players


def print_results(result: TournamentResult) -> None:
    console.print()

    # ── Elo / ratings ──────────────────────────────────────────────────────────
    rating_table = Table(title="Elo Ratings", box=box.SIMPLE_HEAVY, show_lines=False)
    rating_table.add_column("Player", style="bold cyan", no_wrap=True)
    rating_table.add_column("Elo", justify="right")
    rating_table.add_column("Win Rate", justify="right")
    rating_table.add_column("Games", justify="right")

    for rd in sorted(result.ratings_detail.values(), key=lambda r: r.rating, reverse=True):
        rating_table.add_row(
            rd.name,
            f"{rd.rating:.0f}",
            f"{rd.win_rate:.1%}",
            str(rd.games_played),
        )
    console.print(rating_table)

    # ── Head-to-head matchups ──────────────────────────────────────────────────
    matchup_table = Table(
        title="Head-to-Head Matchups",
        box=box.SIMPLE_HEAVY,
        show_lines=True,
        min_width=100,
    )
    matchup_table.add_column("Matchup", style="bold", min_width=26, no_wrap=True)
    matchup_table.add_column("Win% A", justify="right")
    matchup_table.add_column("W-A", justify="right")
    matchup_table.add_column("W-B", justify="right")
    matchup_table.add_column("Draw", justify="right")
    matchup_table.add_column("VP-A", justify="right")
    matchup_table.add_column("VP-B", justify="right")
    matchup_table.add_column("Turns", justify="right")

    for (p1, p2), m in result.matchups.items():
        color = "green" if m.win_rate_a > 0.5 else "red" if m.win_rate_a < 0.5 else "yellow"
        matchup_table.add_row(
            f"{p1}  vs  {p2}",
            f"[{color}]{m.win_rate_a:.1%}[/]",
            str(m.wins_a),
            str(m.wins_b),
            str(m.draws),
            f"{m.avg_vp_a:.1f}",
            f"{m.avg_vp_b:.1f}",
            f"{m.avg_game_length:.1f}",
        )
    console.print(matchup_table)

    # ── Summary ────────────────────────────────────────────────────────────────
    avg_turns = sum(m.avg_game_length for m in result.matchups.values()) / len(result.matchups)
    console.print(
        f"[dim]Total games: {result.total_games} | "
        f"Avg game length: {avg_turns:.1f} turns | "
        f"{result.games_per_second:.1f} games/s | "
        f"Wall time: {result.wall_seconds:.1f}s[/dim]"
    )
    console.print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="BotPlayer strategy round-robin tournament (duchy × province axes)"
    )
    parser.add_argument(
        "--games", type=int, default=200,
        help="Games per matchup side (total = 2×games per pair, default: 200)",
    )
    parser.add_argument(
        "--kingdom", nargs="+", default=None,
        help="Kingdom card names (default: Chapel kingdom)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility",
    )
    parser.add_argument(
        "--prosperity", action="store_true", default=False,
        help="Add Colony and Platinum",
    )
    axis = parser.add_mutually_exclusive_group()
    axis.add_argument(
        "--duchy-only", action="store_true", default=False,
        help="Only vary duchy strategy (fix province at Greedy)",
    )
    axis.add_argument(
        "--province-only", action="store_true", default=False,
        help="Only vary province strategy (fix duchy at Greedy)",
    )
    args = parser.parse_args()

    kingdom = args.kingdom or DEFAULT_KINGDOM
    game_kwargs: dict[str, Any] = {}
    if args.prosperity:
        game_kwargs["prosperity"] = True

    players = build_players(args.duchy_only, args.province_only)
    mode = "duchy only" if args.duchy_only else "province only" if args.province_only else "full 3×2 grid"

    console.print(f"\n[bold]BigMoney Strategy Tournament[/bold]  [dim]({mode})[/dim]")
    console.print(f"Kingdom: [cyan]{', '.join(kingdom)}[/cyan]")
    console.print(
        f"Players: [yellow]{len(players)}[/yellow]  |  "
        f"Games per side: [yellow]{args.games}[/yellow]  "
        f"(total per pair: {args.games * 2})"
    )
    console.print()

    result = run_tournament(
        players=players,
        kingdom_cards=kingdom,
        num_games_per_matchup=args.games,
        seed=args.seed,
        collect_traces=0,
        **game_kwargs,
    )

    print_results(result)


if __name__ == "__main__":
    main()

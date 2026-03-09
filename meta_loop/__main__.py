"""CLI entry point for single-shot heuristic evaluation.

Usage:
    uv run python -m meta_loop --model google/gemini-3-flash-preview
    uv run python -m meta_loop --model deepseek/deepseek-r1 --games 100
    uv run python -m meta_loop --random --model anthropic/claude-sonnet-4.6
    uv run python -m meta_loop --prosperity --kingdom Mountebank ...
    uv run python -m meta_loop --events Advance Alliance --kingdom ...
    uv run python -m meta_loop --tweak path/to/player.py --kingdom Chapel Smithy ...
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from datetime import datetime

from .driver import run_eval
from .kingdom_builder import generate_random_kingdom


DEFAULT_KINGDOM = [
    "Chapel", "Village", "Smithy", "Market", "Militia",
    "Moat", "Festival", "Laboratory", "Workshop", "Witch",
]


def main():
    parser = argparse.ArgumentParser(
        description="Single-shot eval: LLM writes Dominion heuristic, tournament evaluates it"
    )
    parser.add_argument(
        "--kingdom", nargs="+", default=None,
        help="Kingdom card names (default: Chapel kingdom)"
    )
    parser.add_argument(
        "--random", action="store_true", default=False,
        help="Generate a random kingdom using the game engine"
    )
    parser.add_argument(
        "--games", type=int, default=200,
        help="Games per matchup side (total = 2×games per pair) (default: 200)"
    )
    parser.add_argument(
        "--backend", default="openrouter", choices=["openrouter", "ollama"],
        help="LLM backend (default: openrouter)"
    )
    parser.add_argument(
        "--model", default="anthropic/claude-sonnet-4-20250514",
        help="Model name (default: anthropic/claude-sonnet-4-20250514)"
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output", default=None,
        help="Output directory (default: runs/<timestamp>_<model>)"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.3,
        help="LLM temperature (default: 0.3)"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=8192,
        help="LLM max output tokens (default: 8192)"
    )
    parser.add_argument(
        "--tweak", default=None, metavar="FILE",
        help="Path to a target player .py file. The LLM will try to beat it "
             "by making small modifications to its strategy, instead of "
             "writing a strategy from scratch."
    )

    # --- Game setup options (forwarded to Dominion Game constructor) ---
    parser.add_argument(
        "--prosperity", action="store_true", default=False,
        help="Add Colony/Platinum to the supply"
    )
    parser.add_argument(
        "--events", nargs="+", default=[],
        help="Event names to include (e.g. Advance Alliance)"
    )
    parser.add_argument(
        "--num-events", type=int, default=0,
        help="Number of random events to include"
    )
    parser.add_argument(
        "--landmarks", nargs="+", default=[],
        help="Landmark names to include (e.g. Aqueduct Arena)"
    )
    parser.add_argument(
        "--num-landmarks", type=int, default=0,
        help="Number of random landmarks to include"
    )
    parser.add_argument(
        "--ways", nargs="+", default=[],
        help="Way names to include (e.g. 'Way of the Butterfly')"
    )
    parser.add_argument(
        "--num-ways", type=int, default=0,
        help="Number of random ways to include"
    )
    parser.add_argument(
        "--projects", nargs="+", default=[],
        help="Project names to include"
    )
    parser.add_argument(
        "--num-projects", type=int, default=0,
        help="Number of random projects to include"
    )
    parser.add_argument(
        "--allies", nargs="+", default=[],
        help="Ally names to include"
    )
    parser.add_argument(
        "--traits", nargs="+", default=[],
        help="Trait names to include (e.g. Cheap)"
    )
    parser.add_argument(
        "--num-traits", type=int, default=0,
        help="Number of random traits to include"
    )
    parser.add_argument(
        "--prophecies", nargs="+", default=[],
        help="Prophecy names to include"
    )

    args = parser.parse_args()

    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_short = args.model.split("/")[-1].replace(":", "_")
        args.output = os.path.join("runs", f"{timestamp}_{model_short}")

    # Build game_kwargs from CLI args
    game_kwargs: dict = {}
    if args.prosperity:
        game_kwargs["prosperity"] = True
    if args.events:
        game_kwargs["events"] = args.events
    if args.num_events:
        game_kwargs["num_events"] = args.num_events
    if args.landmarks:
        game_kwargs["landmarks"] = args.landmarks
    if args.num_landmarks:
        game_kwargs["num_landmarks"] = args.num_landmarks
    if args.ways:
        game_kwargs["ways"] = args.ways
    if args.num_ways:
        game_kwargs["num_ways"] = args.num_ways
    if args.projects:
        game_kwargs["projects"] = args.projects
    if args.num_projects:
        game_kwargs["num_projects"] = args.num_projects
    if args.allies:
        game_kwargs["allies"] = args.allies
    if args.traits:
        game_kwargs["traits"] = args.traits
    if args.num_traits:
        game_kwargs["num_traits"] = args.num_traits
    if args.prophecies:
        game_kwargs["prophecies"] = args.prophecies

    # Determine kingdom
    if args.random:
        kingdom_seed = args.seed if args.seed is not None else random.randint(0, 2**31 - 1)
        kingdom_cards, effective_kwargs = generate_random_kingdom(
            seed=kingdom_seed, **game_kwargs,
        )
        # Use effective_kwargs (captures what the engine resolved)
        game_kwargs = effective_kwargs
    elif args.kingdom is not None:
        kingdom_cards = args.kingdom
    else:
        kingdom_cards = DEFAULT_KINGDOM

    result = run_eval(
        kingdom_cards=kingdom_cards,
        games_per_eval=args.games,
        llm_backend=args.backend,
        model=args.model,
        seed=args.seed,
        output_dir=args.output,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        game_kwargs=game_kwargs if game_kwargs else None,
        tweak_target=args.tweak,
    )

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()

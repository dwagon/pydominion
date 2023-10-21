#!/usr/bin/env python
""" Run a Dominion Game """
import argparse
import sys

from dominion import Game


###############################################################################
def parse_cli_args(args=None):
    """Parse the command line arguments"""
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Play dominion")
    parser.add_argument("--numplayers", type=int, default=2, help="How many players")
    parser.add_argument(
        "--card",
        action="append",
        dest="initcards",
        default=[],
        help="Include card in lineup",
    )
    parser.add_argument(
        "--bad",
        action="append",
        dest="badcards",
        default=[],
        help="Do not include card in lineup",
    )
    parser.add_argument(
        "--potions",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Use potions",
    )
    parser.add_argument("--shelters", type=bool, default=True, help="Allow shelters")
    parser.add_argument(
        "--num_events", type=int, default=0, help="Number of events to use"
    )
    parser.add_argument(
        "--events", action="append", dest="events", default=[], help="Include event"
    )
    parser.add_argument("--num_ways", type=int, default=0, help="Number of ways to use")
    parser.add_argument(
        "--ways", action="append", dest="ways", default=[], help="Include way"
    )

    parser.add_argument(
        "--num_landmarks", type=int, default=0, help="Number of landmarks to use"
    )
    parser.add_argument(
        "--landmark",
        action="append",
        dest="landmarks",
        default=[],
        help="Include landmark",
    )
    parser.add_argument(
        "--landmark_path", default="dominion/landmarks", help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--num_projects", type=int, default=0, help="Number of projects to use"
    )

    parser.add_argument(
        "--num_traits", type=int, default=0, help="Number of traits to use"
    )
    parser.add_argument(
        "--oldcards",
        action="store_true",
        default=False,
        help="Use cards from retired versions",
    )
    parser.add_argument(
        "--project",
        action="append",
        dest="init_projects",
        default=[],
        help="Include project",
    )
    parser.add_argument(
        "--project_path", default="dominion/projects", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--ally",
        dest="allies",
        action="append",
        default=[],
        help="Include specific ally",
    )

    parser.add_argument(
        "--trait_path", default="dominion/traits", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--trait",
        dest="traits",
        default=[],
        action="append",
        help="Include specific trait",
    )

    parser.add_argument(
        "--cardset",
        type=argparse.FileType("r"),
        help="File containing list of cards to use",
    )
    parser.add_argument("--card_path", default="dominion/cards", help=argparse.SUPPRESS)
    parser.add_argument(
        "--artifact_path", default="dominion/artifacts", help=argparse.SUPPRESS
    )
    parser.add_argument("--boon_path", default="dominion/boons", help=argparse.SUPPRESS)
    parser.add_argument("--num_stacks", default=10, help=argparse.SUPPRESS)
    parser.add_argument(
        "--prosperity",
        default=False,
        action="store_true",
        help="Use colonies and platinum coins",
    )
    parser.add_argument(
        "--bot", action="store_true", dest="bot", default=False, help="Bot Player"
    )
    parser.add_argument(
        "--randobot",
        type=int,
        dest="randobot",
        default=0,
        help="Number of Rando Bot Players",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        dest="quiet",
        default=False,
        help="Supress a lot of output",
    )
    namespace = parser.parse_args(args)
    return namespace


###############################################################################
def run_game(args):  # pragma: no cover
    """TODO"""
    cards = args["initcards"]
    turn = 0
    if args["cardset"]:
        for line in args["cardset"]:
            if line.startswith("#"):
                continue
            if line.startswith("--prosperity"):
                args["prosperity"] = True
                continue
            if line.startswith("--oldcards"):
                args["oldcards"] = True
            cards.append(line.strip())
    args["initcards"] = cards
    g = Game.Game(**args)
    g.start_game()
    try:
        while not g.game_over:
            try:
                turn += 1
                g.turn()
            except Exception:
                g.print_state(card_dump=True)
                raise
            if turn > 400:  # Eternal game
                return
    except KeyboardInterrupt:
        g.game_over = True
    g.whoWon()


###############################################################################
def main():  # pragma: no cover
    """Command line entry point"""
    args = parse_cli_args()
    run_game(vars(args))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    main()

# EOF

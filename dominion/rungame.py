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
    parser.add_argument("--shelters", type=bool, default=True, help="Allow shelters")
    parser.add_argument("--numevents", type=int, default=0, help="Number of events to use")
    parser.add_argument("--events", action="append", dest="eventcards", default=[], help="Include event")
    parser.add_argument("--numways", type=int, default=0, help="Number of ways to use")
    parser.add_argument("--ways", action="append", dest="waycards", default=[], help="Include way")

    parser.add_argument("--numlandmarks", type=int, default=0, help="Number of landmarks to use")
    parser.add_argument(
        "--landmark",
        action="append",
        dest="landmarkcards",
        default=[],
        help="Include landmark",
    )
    parser.add_argument("--landmarkpath", default="dominion/landmarks", help=argparse.SUPPRESS)

    parser.add_argument("--numprojects", type=int, default=0, help="Number of projects to use")
    parser.add_argument(
        "--oldcards",
        action="store_true",
        default=False,
        help="Use cards from retired versions",
    )
    parser.add_argument(
        "--project",
        action="append",
        dest="initprojects",
        default=[],
        help="Include project",
    )
    parser.add_argument("--projectpath", default="dominion/projects", help=argparse.SUPPRESS)
    parser.add_argument(
        "--ally",
        dest="init_ally",
        action="append",
        default=[],
        help="Include specific ally",
    )
    parser.add_argument(
        "--cardset",
        type=argparse.FileType("r"),
        help="File containing list of cards to use",
    )
    parser.add_argument("--cardbase", action="append", help="Include only cards from the specified base")
    parser.add_argument("--cardpath", default="dominion/cards", help="Where to find card definitions")
    parser.add_argument("--artifactpath", default="dominion/artifacts", help=argparse.SUPPRESS)
    parser.add_argument("--boonpath", default="dominion/boons", help=argparse.SUPPRESS)
    parser.add_argument("--numstacks", default=10, help=argparse.SUPPRESS)
    parser.add_argument(
        "--prosperity",
        default=False,
        action="store_true",
        help="Use colonies and platinum coins",
    )
    parser.add_argument("--bot", action="store_true", dest="bot", default=False, help="Bot Player")
    parser.add_argument("--randobot", type=int, dest="randobot", default=0, help="Num Rando Bot Players")
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
def runGame(args):  # pragma: no cover
    """TODO"""
    cards = args["initcards"]
    if args["cardset"]:
        for line in args["cardset"]:
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
        while not g.gameover:
            try:
                g.turn()
            except Exception:
                g.print_state(card_dump=True)
                raise
    except KeyboardInterrupt:
        g.gameover = True
    g.whoWon()


###############################################################################
def main():  # pragma: no cover
    """Command line entry point"""
    args = parse_cli_args()
    runGame(vars(args))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    main()

# EOF

"""Player is a non-interactive bot of no intelligence - randomly select option"""

import random
import sys
from typing import Any

import colorama

from dominion import Piles, Card
from dominion.Option import Option
from dominion.Player import Player

colours = [
    colorama.Fore.RED,
    colorama.Fore.GREEN,
    colorama.Fore.YELLOW,
    colorama.Fore.BLUE,
    colorama.Fore.MAGENTA,
    colorama.Fore.CYAN,
    colorama.Fore.WHITE,
    colorama.Fore.LIGHTBLUE_EX,
    colorama.Fore.LIGHTCYAN_EX,
    colorama.Fore.LIGHTGREEN_EX,
    colorama.Fore.LIGHTMAGENTA_EX,
    colorama.Fore.LIGHTRED_EX,
    colorama.Fore.LIGHTYELLOW_EX,
]


###############################################################################
###############################################################################
###############################################################################
class RandobotPlayer(Player):
    """The Bot"""

    def __init__(self, game, name="", quiet=False, **kwargs):
        colorama.init()
        self.colour = f"{colorama.Back.BLACK}{random.choice(colours)}"
        self.quiet = quiet
        Player.__init__(self, game, name, **kwargs)

    ###########################################################################
    def output(self, msg, end="\n"):
        if not self.quiet:
            sys.stdout.write(f"{self.colour}{self.name}{colorama.Style.RESET_ALL}: ")
            sys.stdout.write(f"{msg}{end}")
        self.messages.append(msg)

    ###########################################################################
    def card_selSource(self, **kwargs):
        """Understand the various places to select cards from - either a
        text description of the source, a list of cards, or by default
        the players hand"""
        if "cardsrc" in kwargs:
            if kwargs["cardsrc"] == "hand":
                select_from = self.piles[Piles.HAND]
            elif kwargs["cardsrc"] == "played":
                select_from = self.piles[Piles.PLAYED]
            elif kwargs["cardsrc"] == "discard":
                select_from = self.piles[Piles.DISCARD]
            else:
                select_from = kwargs["cardsrc"]
        else:
            select_from = self.piles[Piles.HAND]
        return select_from

    ###########################################################################
    def selectorLine(self, o) -> str:
        """User-friendly representation of option"""
        output = []
        if isinstance(o, dict):
            verb = o["print"]
            del o["print"]
            newopt = Option(verb=verb, **o)
            o = newopt
        elif isinstance(o, Option):
            pass
        else:
            print(f"Fail: No idea what {o} {type(o)} is")
            sys.exit(1)
        output.append(o["selector"])
        if o["verb"]:
            output.append(o["verb"])
        if o["name"]:
            output.append(o["name"])
        if o["details"]:
            output.append(f"({o['details']})")
        if o["name"] and not o["details"] and o["desc"]:
            output.append("-")
        if o["notes"]:
            output.append(o["notes"])

        output.append(o["desc"])
        return " ".join(output)

    ###########################################################################
    def user_input(self, options, prompt: str):
        """Handle user input"""
        print(self._generate_prompt())
        for opt in options:
            print(self.selectorLine(opt))
        for opt in options:
            if "action" not in opt:
                break
            if opt["action"] == "spendall" and random.randint(1, 10) < 7:
                print(f"Default spendall {opt=}")
                return opt
            if opt["action"] == "payback":
                print(f"Mandatory payback {opt=}")
                return opt

        # Do anything but quit
        try:
            avail = [_ for _ in options if _["selector"] != "-" and _.get("action") != "quit"]
        except KeyError:
            print(f"{options=}")
            raise
        if avail:
            opt = random.choice(avail)
            print(f"Random: {opt=}")
            return opt

        # If only quit is available then quit
        for opt in options:
            if opt["action"] == "quit":
                print(f"Quit {opt=}")
                return opt

        # How did we get here?
        print(f"user_input - fail. {options=}")
        return None

    ###########################################################################
    def card_sel(self, num: int = 1, **kwargs: Any) -> list[Card.Card] | None:
        """Select a card at random"""
        print(f"card_sel {self.currcards} {kwargs=}")
        cards = self.card_selSource(**kwargs)
        if not cards:
            return None
        card = random.choice(cards)
        print(f"card_sel chose: {card=}")
        return [card]

    ###########################################################################
    def card_pile_sel(self, num: int = 1, **kwargs: Any) -> list[str] | None:
        """Select a card pile at random"""
        print(f"card_pile_sel {kwargs=}")
        cards = list(self.game.card_piles.keys())
        if not cards:
            return None
        print(f"card_pile_sel {cards=}")
        card = random.choice(cards)
        print(f"card_pile_sel {card=}")
        return [card]

    ###########################################################################
    def plr_choose_options(self, prompt, *choices):
        print(f"plr_choose_options {self.currcards} {prompt=} {choices=}")
        choice = random.choice(choices)
        print(f"plr_choose_options {self.currcards} {choice=}")
        return choice[1]

    ###########################################################################
    def pick_to_discard(self, numtodiscard: int, keepvic: bool = False):
        """Many attacks require this sort of response.
        Return num cards to discard"""
        if numtodiscard <= 0:
            return []
        to_discard = []

        # Discard non-treasures first
        for card in self.piles[Piles.HAND]:
            if card.isTreasure():
                continue
            if keepvic and card.isVictory():
                continue
            to_discard.append(card)
        if len(to_discard) >= numtodiscard:
            return to_discard[:numtodiscard]

        # Discard the cheapest treasures next
        while len(to_discard) < numtodiscard:
            for treas in ("Copper", "Silver", "Gold"):
                for card in self.piles[Piles.HAND]:
                    if card.name == treas:
                        to_discard.append(card)
        if len(to_discard) >= numtodiscard:
            return to_discard[:numtodiscard]
        hand = ", ".join([_.name for _ in self.piles[Piles.HAND]])
        sys.stderr.write(f"Couldn't find cards to discard {numtodiscard} from {hand}")
        sys.stderr.write(f"Managed to get {(', '.join([_.name for _ in to_discard]))} so far\n")


# EOF

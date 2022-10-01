""" Player is a non-interactive bot of no intelligence - randomly select option """
import sys
import random
import colorama
from dominion.Player import Player

if sys.version[0] == "3":  # pragma: no cover
    raw_input = input


###############################################################################
###############################################################################
###############################################################################
class RandobotPlayer(Player):
    """The Bot"""

    def __init__(self, game, name="", quiet=False, **kwargs):
        colorama.init()
        self.colour = f"{colorama.Back.BLACK}{colorama.Fore.MAGENTA}"
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
        text desctiption of the source, a list of cards, or by default
        the players hand"""
        if "cardsrc" in kwargs:
            if kwargs["cardsrc"] == "hand":
                selectfrom = self.hand
            elif kwargs["cardsrc"] == "played":
                selectfrom = self.played
            elif kwargs["cardsrc"] == "discard":
                selectfrom = self.discardpile
            else:
                selectfrom = kwargs["cardsrc"]
        else:
            selectfrom = self.hand
        return selectfrom

    ###########################################################################
    def user_input(self, options, prompt):
        """Handle user input"""
        for opt in options:
            if "action" not in opt:
                break
            if opt["action"] == "spendall":
                print(f"{opt=}")
                return opt
            if opt["action"] == "payback":
                print(f"{opt=}")
                return opt

        # Do anything but quit
        try:
            avail = [_ for _ in options if _["selector"] != "-" and _.get("action") != "quit"]
        except KeyError:
            print(f"{options=}")
            raise
        if avail:
            opt = random.choice(avail)
            print(f"{opt=}")
            return opt

        # If only quit is available then quit
        for opt in options:
            if opt["action"] == "quit":
                print(f"{opt=}")
                return opt

    ###########################################################################
    def card_sel(self, num=1, **kwargs):
        """Select a card at random"""
        print(f"card_sel {kwargs=}")
        cards = self.card_selSource(**kwargs)
        print(f"card_sel {cards=}")
        card = random.choice(cards)
        print(f"card_sel {card=}")
        return [card]

    ###########################################################################
    def plr_choose_options(self, prompt, *choices):
        print(f"plr_choose_options {choices=}")
        choice = random.choice(choices)
        print(f"plr_choose_options {choice=}")
        return choice[1]

    ###########################################################################
    def pick_to_discard(self, numtodiscard, keepvic=False):
        """Many attacks require this sort of response.
        Return num cards to discard"""
        if numtodiscard <= 0:
            return []
        todiscard = []

        # Discard non-treasures first
        for card in self.hand:
            if card.isTreasure():
                continue
            if keepvic and card.isVictory():
                continue
            todiscard.append(card)
        if len(todiscard) >= numtodiscard:
            return todiscard[:numtodiscard]

        # Discard cheapest treasures next
        while len(todiscard) < numtodiscard:
            for treas in ("Copper", "Silver", "Gold"):
                for card in self.hand:
                    if card.name == treas:
                        todiscard.append(card)
        if len(todiscard) >= numtodiscard:
            return todiscard[:numtodiscard]
        sys.stderr.write(
            f"Couldn't find cards to discard {numtodiscard} from {', '.join([_.name for _ in self.hand])}"
        )
        sys.stderr.write(f"Managed to get {(', '.join([_.name for _ in todiscard]))} so far\n")


# EOF

""" Player is a non-interactive bot of dubious intelligence - big money strategy """
import inspect
import sys
import colorama
from dominion.Player import Player
from dominion import Piles

if sys.version[0] == "3":  # pragma: no cover
    raw_input = input


###############################################################################
###############################################################################
###############################################################################
class BotPlayer(Player):
    """The Bot"""

    def __init__(self, game, name="", quiet=False, **kwargs):
        colorama.init()
        self.colour = f"{colorama.Back.BLACK}{colorama.Fore.RED}"
        self.quiet = quiet
        Player.__init__(self, game, name, **kwargs)

    ###########################################################################
    def output(self, msg, end="\n"):
        if not self.quiet:
            sys.stdout.write(f"{self.colour}{self.name}{colorama.Style.RESET_ALL}: ")
            sys.stdout.write(f"{msg}{end}")
        self.messages.append(msg)

    ###########################################################################
    @classmethod
    def get_options(cls, options):
        try:
            opts = {}
            for opt in options:
                if opt["action"] == "buy":
                    if opt["card"].name == "Colony":
                        opts["colony"] = opt
                    if opt["card"].name == "Province":
                        opts["province"] = opt
                    if opt["card"].name == "Platinum":
                        opts["platinum"] = opt
                    if opt["card"].name == "Gold":
                        opts["gold"] = opt
                    if opt["card"].name == "Duchy":
                        opts["duchy"] = opt
                    if opt["card"].name == "Silver":
                        opts["silver"] = opt
                if opt["action"] == "quit":
                    opts["quit"] = opt
                if opt["action"] == "spendall":
                    opts["spendall"] = opt
            return opts
        except KeyError as exc:  # pragma: no cover
            print(f"Options={options}")
            print(f"Exception: {str(exc)}")
            raise

    ###########################################################################
    def user_input(self, options, prompt):  # pylint: disable=too-many-return-statements
        opts = self.get_options(options)
        if "spendall" in opts:
            return opts["spendall"]
        if self.buys.get() == 0:
            return opts["quit"]
        coin = self.coins.get()
        self.output(f"Have {coin} coins")
        if coin >= 11 and "colony" in opts:
            return opts["colony"]
        if coin >= 9 and "platinum" in opts:
            return opts["platinum"]
        if coin >= 8:
            return opts["province"]
        if coin >= 6 and "gold" in opts:
            return opts["gold"]
        if coin >= 5 and "duchy" in opts:
            return opts["duchy"]
        if coin >= 3 and "silver" in opts:
            return opts["silver"]
        return opts["quit"]

    ###########################################################################
    @classmethod
    def getCallingCard(cls):
        """Get the module that represents the card doing requiring the response"""
        stack = inspect.stack()
        for rec in stack:
            mod = inspect.getmodule(rec[0])
            mod_name = mod.__name__.replace("dominion.", "")
            if mod_name not in ("BotPlayer", "Player", "__main__"):
                mod = inspect.getmodule(rec[0])
                return mod
        return None

    ###########################################################################
    def card_sel(self, num=1, **kwargs):
        mod = self.getCallingCard()
        if hasattr(mod, "botresponse"):
            return mod.botresponse(self, "cards", kwargs=kwargs)
        assert False, f"BigMoneyBot can't select cards from {mod.__name__}"

    ###########################################################################
    def plr_choose_options(self, prompt, *choices):
        mod = self.getCallingCard()
        if hasattr(mod, "botresponse"):
            return mod.botresponse(self, "choices", args=choices)
        assert False, f"BigMoneyBot can't choose options from {mod.__name__}"

    ###########################################################################
    def pick_to_discard(self, num_to_discard, keepvic=False):
        """Many attacks require this sort of response.
        Return num cards to discard"""
        if num_to_discard <= 0:
            return []
        todiscard = []

        # Discard non-treasures first
        for card in self.piles[Piles.HAND]:
            if card.isTreasure():
                continue
            if keepvic and card.isVictory():
                continue
            todiscard.append(card)
        if len(todiscard) >= num_to_discard:
            return todiscard[:num_to_discard]

        # Discard the cheapest treasures next
        while len(todiscard) < num_to_discard:
            for treas in ("Copper", "Silver", "Gold"):
                for card in self.piles[Piles.HAND]:
                    if card.name == treas:
                        todiscard.append(card)
        if len(todiscard) >= num_to_discard:
            return todiscard[:num_to_discard]
        sys.stderr.write(
            f"Couldn't find cards to discard {num_to_discard} from {', '.join([_.name for _ in self.piles[Piles.HAND]])}"
        )
        sys.stderr.write(
            f"Managed to get {(', '.join([_.name for _ in todiscard]))} so far\n"
        )


# EOF

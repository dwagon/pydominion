import inspect
import sys
import colorama
from dominion.Player import Player

if sys.version[0] == "3":  # pragma: no cover
    raw_input = input


###############################################################################
###############################################################################
###############################################################################
class BotPlayer(Player):
    def __init__(self, game, name="", quiet=False, **kwargs):
        colorama.init()
        self.colour = "%s%s" % (colorama.Back.BLACK, colorama.Fore.RED)
        self.quiet = quiet
        Player.__init__(self, game, name, **kwargs)

    ###########################################################################
    def output(self, msg, end="\n"):
        if not self.quiet:
            sys.stdout.write(
                "%s%s%s: " % (self.colour, self.name, colorama.Style.RESET_ALL)
            )
            sys.stdout.write("%s%s" % (msg, end))
        self.messages.append(msg)

    ###########################################################################
    def getOptions(self, options):
        try:
            opts = {}
            for o in options:
                if o["action"] == "buy" and o["card"].name == "Colony":
                    opts["colony"] = o
                if o["action"] == "buy" and o["card"].name == "Province":
                    opts["province"] = o
                if o["action"] == "buy" and o["card"].name == "Platinum":
                    opts["platinum"] = o
                if o["action"] == "buy" and o["card"].name == "Gold":
                    opts["gold"] = o
                if o["action"] == "buy" and o["card"].name == "Duchy":
                    opts["duchy"] = o
                if o["action"] == "buy" and o["card"].name == "Silver":
                    opts["silver"] = o
                if o["action"] == "quit":
                    opts["quit"] = o
                if o["action"] == "spendall":
                    opts["spendall"] = o
            return opts
        except KeyError as exc:  # pragma: no cover
            print("Options=%s" % options)
            print("Exception: %s" % str(exc))
            raise

    ###########################################################################
    def user_input(self, options, prompt):  # pylint: disable=too-many-return-statements
        opts = self.getOptions(options)
        if "spendall" in opts:
            return opts["spendall"]
        if self.get_buys() == 0:
            return opts["quit"]
        coin = self.get_coins()
        self.output("Have %d coins" % coin)
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
    def getCallingCard(self):
        """Get the module that represents the card doing requiring the response"""
        stack = inspect.stack()
        for st in stack:
            mod = inspect.getmodule(st[0])
            mod_name = mod.__name__.replace('dominion.', '')
            if mod_name not in ("BotPlayer", "Player", "__main__"):
                mod = inspect.getmodule(st[0])
                return mod
        return None

    ###########################################################################
    def cardSel(self, num=1, **kwargs):
        mod = self.getCallingCard()
        if hasattr(mod, "botresponse"):
            return mod.botresponse(self, "cards", kwargs=kwargs)
        assert False, "BigMoneyBot can't select cards from %s" % mod.__name__
        return None

    ###########################################################################
    def plr_choose_options(self, prompt, *choices):
        mod = self.getCallingCard()
        if hasattr(mod, "botresponse"):
            return mod.botresponse(self, "choices", args=choices)
        assert False, "BigMoneyBot can't choopse options from %s" % mod.__name__
        return None

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
                for card in self.hand[:]:
                    if card.name == treas:
                        todiscard.append(card)
        if len(todiscard) >= numtodiscard:
            return todiscard[:numtodiscard]
        sys.stderr.write(
            "Couldn't find cards to discard %d from %s\n"
            % (numtodiscard, ", ".join([c.name for c in self.hand]))
        )
        sys.stderr.write(
            "Managed to get %s so far\n" % (", ".join([c.name for c in todiscard]))
        )


# EOF

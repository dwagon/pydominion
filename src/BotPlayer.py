import sys
import colorama
from Player import Player
import inspect

if sys.version[0] == "3":
    raw_input = input


###############################################################################
###############################################################################
###############################################################################
class BotPlayer(Player):
    def __init__(self, game, name='', quiet=False, **kwargs):
        colorama.init()
        self.colour = "%s%s" % (colorama.Back.BLACK, colorama.Fore.RED)
        self.quiet = quiet
        Player.__init__(self, game, name)

    ###########################################################################
    def output(self, msg, end='\n'):
        if not self.quiet:
            sys.stdout.write("%s%s%s: " % (self.colour, self.name, colorama.Style.RESET_ALL))
            sys.stdout.write("%s%s" % (msg, end))
        self.messages.append(msg)

    ###########################################################################
    def getOptions(self, options):
        try:
            opts = {}
            for o in options:
                if o['action'] == 'buy' and o['card'].name == 'Province':
                    opts['province'] = o
                if o['action'] == 'buy' and o['card'].name == 'Gold':
                    opts['gold'] = o
                if o['action'] == 'buy' and o['card'].name == 'Duchy':
                    opts['duchy'] = o
                if o['action'] == 'buy' and o['card'].name == 'Silver':
                    opts['silver'] = o
                if o['action'] == 'quit':
                    opts['quit'] = o
                if o['action'] == 'spendall':
                    opts['spendall'] = o
            return opts
        except KeyError as exc:
            print "Options=%s" % options
            print "Exception: %s" % str(exc)
            raise

    ###########################################################################
    def userInput(self, options, prompt):
        opts = self.getOptions(options)
        if 'spendall' in opts:
            return opts['spendall']
        if self.getBuys() == 0:
            return opts['quit']
        coin = self.getCoin()
        self.output("Have %d coins" % coin)
        if coin >= 8:
            return opts['province']
        if coin >= 6:
            return opts['gold']
        if coin >= 5:
            return opts['duchy']
        if coin >= 3:
            return opts['silver']
        return opts['quit']

    ###########################################################################
    def getCallingCard(self):
        """ Get the module that represents the card doing requiring the response """
        stack = inspect.stack()
        for st in stack:
            mod = inspect.getmodule(st[0])
            if mod.__name__ not in ('BotPlayer', 'Player', '__main__'):
                mod = inspect.getmodule(st[0])
                return mod

    ###########################################################################
    def cardSel(self, num=1, **kwargs):
        mod = self.getCallingCard()
        if hasattr(mod, 'botresponse'):
            ans = mod.botresponse(self, 'cards', kwargs=kwargs)
            return ans
        assert False, "BigMoneyBot can't select cards from %s" % mod.__name__

    ###########################################################################
    def plrChooseOptions(self, prompt, *choices):
        mod = self.getCallingCard()
        if hasattr(mod, 'botresponse'):
            ans = mod.botresponse(self, 'choices', args=choices)
            return ans
        assert False, "BigMoneyBot can't choopse options from %s" % mod.__name__

    ###########################################################################
    def pick_to_discard(self, numtodiscard):
        """ Return num cards to discard """
        if numtodiscard <= 0:
            return []
        todiscard = []

        # Discard non-treasures first
        for card in self.hand:
            if not card.isTreasure():
                todiscard.append(card)
        if len(todiscard) >= numtodiscard:
            return todiscard[:2]
        for treas in ('Copper', 'Silver', 'Gold'):
            while len(todiscard) < numtodiscard:
                for card in self.hand:
                    if card.name == treas:
                        todiscard.append(card)
        if len(todiscard) >= numtodiscard:
            return todiscard[:2]
        print "Couldn't find cards to discard from %s" % (", ".join([c.name for c in self.hand]))


# EOF

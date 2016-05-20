import sys
import colorama
from Player import Player

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

    ###########################################################################
    def userInput(self, options, prompt):
        opts = self.getOptions(options)
        if 'spendall' in opts:
            return opts['spendall']
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
    def cardSel(self, num=1, **kwargs):
        import inspect
        stack = inspect.stack()
        parent = stack[3][0]
        mod = inspect.getmodule(parent)
        if hasattr(mod, 'botresponse'):
            ans = mod.botresponse(hand=self.hand)
            return ans
        assert False, "BigMoneyBot can't select cards from %s" % mod.__name__

    ###########################################################################
    def plrChooseOptions(self, prompt, *choices):
        index = 0
        options = []
        for prnt, ans in choices:
            sel = '%s' % index
            options.append({'selector': sel, 'print': prnt, 'answer': ans})
            index += 1
        o = self.userInput(options, prompt)
        return o['answer']

# EOF

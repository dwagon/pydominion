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
    def userInput(self, options, prompt):
        for o in options:
            if o['action'] == 'spendall':
                return o
        coin = self.getCoin()
        self.output("Have %d coins" % coin)
        if coin >= 8:
            for o in options:
                if o['action'] == 'buy' and o['card'].name == 'Province':
                    return o
        if coin >= 6:
            for o in options:
                if o['action'] == 'buy' and o['card'].name == 'Gold':
                    return o
        if coin >= 6:
            for o in options:
                if o['action'] == 'buy' and o['card'].name == 'Duchy':
                    return o
        if coin >= 3:
            for o in options:
                if o['action'] == 'buy' and o['card'].name == 'Silver':
                    return o
        for o in options:
            if o['action'] == 'quit':
                return o

    ###########################################################################
    def cardSel(self, num=1, **kwargs):
        """ Big Money bot should never require this """
        return None

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

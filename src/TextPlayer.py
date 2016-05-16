import sys
import colorama
from Player import Player

if sys.version[0] == "3":
    raw_input = input

colours = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE]


###############################################################################
###############################################################################
###############################################################################
class TextPlayer(Player):
    def __init__(self, game, name='', quiet=False, **kwargs):
        colorama.init()
        self.colour = colours[kwargs['number']]
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
            self.output("%s)    %s" % (o['selector'], o['print']))
        self.output(prompt, end=' ')
        while(1):
            if self.test_input:
                inp = self.test_input.pop(0)
                self.output("Using '%s' test input" % inp)
            else:
                try:
                    inp = raw_input()
                except IOError:
                    self.game.print_state()
                    raise
            if inp:
                matching = []
                for o in options:
                    if o['selector'] == inp:
                        return o
                    if inp.lower() in o['print'].lower():
                        matching.append(o)
                if len(matching) == 1:
                    return matching[0]
            self.output("Invalid Option (%s)" % inp)

    ###########################################################################
    def cardSel(self, num=1, **kwargs):
        """ Most interactions with players are the selection of cards
            either from the hand, the drawpiles, or a subset
            * force
                True - Have to select num cards
                False - Can pick less than num cards [Default]
            * chooser - Which player does the selecting [player]
            * cardsrc
                hand - Select the cards from the players hand
                played - Select the cards from the cards played
            * exclude = [] - Don't let cards in this list be selected
            * printcost
                True - Print out the cost of the cards
                False - Don't print out the cost [Default]
            * verbs
                ('Select', 'Unselect')
            * prompt
                What to tell the player at the start
            * anynum
                True - Any number of cards can be selected
        """
        if 'cardsrc' in kwargs:
            if kwargs['cardsrc'] == 'hand':
                selectfrom = self.hand
            elif kwargs['cardsrc'] == 'played':
                selectfrom = self.played
            else:
                selectfrom = kwargs['cardsrc']
        else:
            selectfrom = self.hand
        if 'chooser' in kwargs and kwargs['chooser']:
            chooser = kwargs['chooser']
        else:
            chooser = self
        if 'force' in kwargs and kwargs['force']:
            force = True
        else:
            force = False
        if 'verbs' in kwargs:
            verbs = kwargs['verbs']
        else:
            verbs = ('Select', 'Unselect')

        if 'prompt' in kwargs:
            chooser.output(kwargs['prompt'])

        if 'anynum' in kwargs and kwargs['anynum']:
            anynum = True
            num = 0
        else:
            anynum = False

        selected = []
        while(True):
            options = []
            if anynum or (force and num == len(selected)) or (not force and num >= len(selected)):
                options.append({'selector': '0', 'print': 'Finish Selecting', 'card': None})
            index = 1
            for c in selectfrom:
                if 'exclude' in kwargs and c.name in kwargs['exclude']:
                    continue
                sel = "%d" % index
                index += 1
                if c not in selected:
                    verb = verbs[0]
                else:
                    verb = verbs[1]
                pr = "%s %s" % (verb, c.name)
                if 'printcost' in kwargs and kwargs['printcost']:
                    pr += " (%d coin)" % chooser.cardCost(c)
                options.append({'selector': sel, 'print': pr, 'card': c})
            o = chooser.userInput(options, "Select which card?")
            if not o['card']:
                break
            if o['card'] in selected:
                selected.remove(o['card'])
            else:
                selected.append(o['card'])
            if num == 1 and len(selected) == 1:
                break
        return selected

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

import sys
from Player import Player

if sys.version[0] == "3":
    raw_input = input


###############################################################################
###############################################################################
###############################################################################
class TextPlayer(Player):
    def __init__(self, game, name='', quiet=False):
        Player.__init__(self, game, name, quiet)

    ###########################################################################
    def output(self, msg, end='\n'):
        if not self.quiet:
            sys.stdout.write("%s: %s%s" % (self.name, msg, end))
        self.messages.append(msg)

    ###########################################################################
    def userInput(self, options, prompt):
        for o in options:
            self.output("%s)\t%s" % (o['selector'], o['print']))
        self.output(prompt, end=' ')
        while(1):
            if self.test_input:
                inp = self.test_input.pop(0)
                self.output("Using '%s' test input" % inp)
            else:
                inp = raw_input()
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
    def turn(self):
        self.startTurn()
        self.output("#" * 50)
        stats = "(%d points, %d cards)" % (self.getScore(), self.countCards())
        self.output("%s Turn %s" % (self.name, stats))
        while(1):
            if self.hand:
                self.output("Hand: %s" % ", ".join([c.name for c in self.hand]))
            else:
                self.output("Hand: <EMPTY>")
            if self.played:
                self.output("Played: %s" % ", ".join([c.name for c in self.played]))
            else:
                self.output("Played: <NONE>")

            opt = self.choiceSelection()
            if opt['action'] == 'buy':
                self.buyCard(opt['card'])
            elif opt['action'] == 'event':
                self.performEvent(opt['card'])
            elif opt['action'] == 'coin':
                self.spendCoin()
            elif opt['action'] == 'play':
                self.playCard(opt['card'])
            elif opt['action'] == 'spend':
                self.playCard(opt['card'])
            elif opt['action'] == 'spendall':
                self.spendAllCards()
            elif opt['action'] == 'quit':
                break
            else:
                sys.stderr.write("ERROR: Unhandled action %s" % opt['action'])
        self.endTurn()

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

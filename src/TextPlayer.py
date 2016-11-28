import sys
import colorama
from Player import Player
from Msg import Msg, Option

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
            if isinstance(msg, Msg):
                sys.stdout.write("%s%s" % (msg, end))
            else:
                sys.stdout.write("%s%s" % (msg, end))
        self.messages.append(msg)

    ###########################################################################
    def wrap(self, text, first=0, indent=15, maxwidth=75):
        """ Wrap the text so that it doesn't take more than maxwidth chars.
        The first line already has "first" characters in it. Subsequent lines
        should be indented "indent" spaces
        """
        outstr = []
        sentence = []
        for word in text.split():
            if len(" ".join(sentence)) + len(word) + first > maxwidth:
                outstr.append(" ".join(sentence))
                sentence = [" " * indent, word]
                first = 0
            else:
                sentence.append(word.strip())
        outstr.append(" ".join(sentence))
        return "\n".join(outstr)

    ###########################################################################
    def selectorLine(self, o):
        output = []
        output.append("%s)" % o['selector'])
        if o['verb']:
            output.append(o['verb'])
        if o['name']:
            output.append(o['name'])
        if o['details']:
            output.append("(%s)" % o['details'])

        first = len(" ".join(output))
        strout = self.wrap(o['desc'], first=first, indent=len(self.name)+4)
        output.append(strout)
        return " ".join(output)

    ###########################################################################
    def userInput(self, options, prompt):
        for o in options:
            line = self.selectorLine(o)
            o.line = line
            self.output(line)
        self.output(prompt, end=' ')
        while(1):
            if self.test_input:
                inp = self.test_input.pop(0)
                self.output("Using '%s' test input" % inp)
            else:
                try:
                    inp = raw_input()
                except (IOError, KeyboardInterrupt):
                    self.game.print_state()
                    raise
            if inp:
                matching = []
                for o in options:
                    if o['selector'] == inp:
                        return o
                    if inp.lower() in o['line'].lower() and o['selector'] != '-':
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
            * cardsrc
                hand - Select the cards from the players hand
                played - Select the cards from the cards played
                discard - Select the cards from the discardpile
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
            elif kwargs['cardsrc'] == 'discard':
                selectfrom = self.discardpile
            else:
                selectfrom = kwargs['cardsrc']
        else:
            selectfrom = self.hand
        if 'force' in kwargs and kwargs['force']:
            force = True
        else:
            force = False
        if 'verbs' in kwargs:
            verbs = kwargs['verbs']
        else:
            verbs = ('Select', 'Unselect')

        if 'prompt' in kwargs:
            self.output(kwargs['prompt'])

        if 'anynum' in kwargs and kwargs['anynum']:
            anynum = True
            num = 0
        else:
            anynum = False

        selected = []
        while(True):
            options = []
            if anynum or (force and num == len(selected)) or (not force and num >= len(selected)):
                o = Option(selector='0', verb='Finish Selecting', card=None)
                options.append(o)
            index = 1
            for c in sorted(selectfrom):
                if 'exclude' in kwargs and c.name in kwargs['exclude']:
                    continue
                sel = "%d" % index
                index += 1
                if c not in selected:
                    verb = verbs[0]
                else:
                    verb = verbs[1]
                o = Option(selector=sel, verb=verb, card=c, name=c.name)
                if 'printcost' in kwargs and kwargs['printcost']:
                    o['desc'] = self.cardCost(c)
                options.append(o)
            o = self.userInput(options, "Select which card?")
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

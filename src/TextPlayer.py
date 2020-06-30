import sys
import colorama
from Player import Player
from Option import Option

if sys.version[0] == "3":
    raw_input = input

colours = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN]


###############################################################################
###############################################################################
###############################################################################
class TextPlayer(Player):
    def __init__(self, game, name='', quiet=False, **kwargs):
        colorama.init()
        self.colour = colours[kwargs['number']]
        self.quiet = quiet
        del kwargs['number']
        Player.__init__(self, game, name, **kwargs)

    ###########################################################################
    def output(self, msg, end='\n'):
        if not self.quiet:
            sys.stdout.write("%s%s%s: " % (self.colour, self.name, colorama.Style.RESET_ALL))
            try:
                sys.stdout.write("%s: " % (self.currcards[0].name))
            except IndexError:
                pass
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
        if not text:
            return ""
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
        if isinstance(o, dict):
            verb = o['print']
            del o['print']
            newopt = Option(verb=verb, **o)
            o = newopt
        elif isinstance(o, Option):
            pass
        else:
            sys.stderr.write("o is %s\n" % type(o))
        output.append("%s)" % o['selector'])
        if o['verb']:
            output.append(o['verb'])
        if o['name']:
            output.append(o['name'])
        if o['details']:
            output.append("(%s)" % o['details'])
        if o['name'] and not o['details'] and o['desc']:
            output.append("-")
        if o['notes']:
            output.append(o['notes'])

        first = len(" ".join(output))
        indent = len(self.name) + 4
        try:
            indent += len(self.currcards[0].name)
        except IndexError:
            pass
        strout = self.wrap(o['desc'], first=first, indent=indent)
        output.append(strout)
        return " ".join(output)

    ###########################################################################
    def userInput(self, options, prompt):
        for o in options:
            line = self.selectorLine(o)
            o['line'] = line
            self.output(line)
        self.output(prompt, end=' ')
        while True:
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
    def cardSelSource(self, **kwargs):
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
        return selectfrom

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
        selectfrom = self.cardSelSource(**kwargs)
        force = kwargs['force'] if 'force' in kwargs else False
        showdesc = kwargs['showdesc'] if 'showdesc' in kwargs else True
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
        types = kwargs['types'] if 'types' in kwargs else {}
        types = self.typeSelector(types)
        while True:
            options = []
            if anynum or (force and num == len(selected)) or (not force and num >= len(selected)):
                o = Option(selector='0', verb='Finish Selecting', card=None)
                options.append(o)
            index = 1
            for c in sorted(selectfrom):
                if 'exclude' in kwargs and c.name in kwargs['exclude']:
                    continue
                if not self.select_by_type(c, types):
                    continue
                sel = "%d" % index
                index += 1
                if c not in selected:
                    verb = verbs[0]
                else:
                    verb = verbs[1]
                o = Option(selector=sel, verb=verb, card=c, name=c.name)
                if showdesc:
                    o['desc'] = c.description(self)
                if 'printcost' in kwargs and kwargs['printcost']:
                    o['details'] = str(self.cardCost(c))
                options.append(o)
            ui = self.userInput(options, "Select which card?")
            if not ui['card']:
                break
            if ui['card'] in selected:
                selected.remove(ui['card'])
            else:
                selected.append(ui['card'])
            if num == 1 and len(selected) == 1:
                break
        return selected

    ###########################################################################
    def plrChooseOptions(self, prompt, *choices):
        index = 0
        options = []
        for prnt, ans in choices:
            options.append(Option(selector='%s' % index, verb=prnt, answer=ans))
            index += 1
        o = self.userInput(options, prompt)
        return o['answer']

# EOF

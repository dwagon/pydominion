import sys
from Player import Player


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
                self.output("Using %s test input" % inp)
            else:
                inp = raw_input()
            for o in options:
                if o['selector'] == inp:
                    return o
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
    def plrTrashCard(self, num=1, anynum=False, printcost=False, force=False, exclude=[]):
        """ Ask player to trash num cards
            force - must trash a card, otherwise have option not to trash
            printcost - print the cost of the card being trashed
            exclude - can't select a card in the exclude list to be trashed
        """
        if anynum:
            self.output("Trash any cards")
        else:
            self.output("Trash %d cards" % num)
        trash = []
        while(True):
            options = []
            if num == len(trash) or not force or anynum:
                options = [{'selector': '0', 'print': 'Finish Trashing', 'card': None}]
            index = 1
            for c in self.hand:
                if exclude and c.name in exclude:
                    continue
                sel = "%d" % index
                if c in trash:
                    verb = "Untrash"
                else:
                    verb = "Trash"
                pr = "%s %s" % (verb, c.name)
                if printcost:
                    pr += " (%d gold)" % self.cardCost(c)
                options.append({'selector': sel, 'print': pr, 'card': c})
                index += 1
            o = self.userInput(options, "Trash which card?")
            if not o['card']:
                break
            trash.append(o['card'])
            if num == 1 and len(trash) == 1:
                break
        for c in trash:
            self.trashCard(c)
        return trash

    ###########################################################################
    def plrGainCard(self, cost, modifier='less', types={}, chooser=None, force=False, destination='discard'):
        """ Gain a card of 'chooser's choice up to cost gold
        if actiononly then gain only action cards
        """
        types = self.typeSelector(types)
        if not chooser:
            chooser = self
        options = []
        if not force:
            options.append({'selector': '0', 'print': 'Nothing', 'card': None})
        if modifier == 'less':
            self.output("Gain a card costing up to %d" % cost)
            buyable = self.cardsUnder(cost, types=types)
        elif modifier == 'equal':
            self.output("Gain a card costing exactly %d" % cost)
            buyable = self.cardsWorth(cost, types=types)
        else:
            self.output("Unhandled modifier: %s" % modifier)
        index = 1
        for p in buyable:
            if not p.purchasable:
                continue
            selector = "%d" % index
            toprint = 'Get %s (%s) %s' % (p.name, self.coststr(p), p.desc)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1

        o = chooser.userInput(options, "What card do you wish?")
        if o['card']:
            self.addCard(o['card'].remove(), destination)
            return o['card']

    ###########################################################################
    def plrDiscardCards(self, num=1, anynum=False):
        """ Get the player to discard exactly num cards """
        discard = []
        while(True):
            options = []
            if anynum or num == len(discard) or len(self.hand) == len(discard):
                options = [{'selector': '0', 'print': 'Finished selecting', 'card': None}]
            index = 1
            for c in self.hand:
                sel = "%s" % index
                pr = "%s %s" % ("Undiscard" if c in discard else "Discard", c.name)
                options.append({'selector': sel, 'print': pr, 'card': c})
                index += 1

            if anynum:
                msg = "Discard which cards."
            else:
                msg = "Discard %s more cards." % (num - len(discard))
            o = self.userInput(options, msg)
            if o['card']:
                if o['card'] in discard:
                    discard.remove(o['card'])
                else:
                    discard.append(o['card'])
            if o['card'] is None:
                break
        for c in discard:
            self.output("Discarding %s" % c.name)
            self.discardCard(c)
        return discard

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

    ###########################################################################
    def plrDiscardDownTo(self, num):
        """ Get the player to discard down to num cards in their hand """
        numtogo = len(self.hand) - num
        self.plrDiscardCards(numtogo)

#EOF

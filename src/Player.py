import operator
import random
import sys

playerNames = ['Adam', 'Alan', 'Alexander', 'Amanda', 'Amy', 'Andrew', 'Angela',
               'Anne', 'Anthony', 'Barbara', 'Benjamin', 'Brian',
               'Catherine', 'Chloe', 'Christine', 'Christopher',
               'Colin', 'Craig', 'Daniel', 'Darren', 'David',
               'Elizabeth', 'Emily', 'Emma', 'Fiona', 'Gary',
               'Geoffrey', 'George', 'Graeme', 'Gregory', 'Heather',
               'Helen', 'Ian', 'Jack', 'James', 'Jason', 'Jennifer',
               'Jessica', 'Joan', 'Joanne', 'John', 'Joshua',
               'Judith', 'Julie', 'Karen', 'Kate', 'Kathleen',
               'Kenneth', 'Kevin', 'Lachlan', 'Laura', 'Lauren',
               'Leanne', 'Linda', 'Lisa', 'Luke', 'Lynette',
               'Margaret', 'Maria', 'Mark', 'Mary', 'Matthew',
               'Melissa', 'Michael', 'Michelle', 'Natalie', 'Nathan',
               'Nicholas', 'Nicole', 'Olivia', 'Pamela', 'Patricia',
               'Paul', 'Peter', 'Raymond', 'Rebecca', 'Richard',
               'Robert', 'Robyn', 'Ronald', 'Ryan', 'Samantha',
               'Samuel', 'Sandra', 'Sarah', 'Scott', 'Shane',
               'Sharon', 'Shirley', 'Simon', 'Stephanie', 'Stephen',
               'Steven', 'Susan', 'Suzanne', 'Thomas', 'Timothy',
               'Wayne', 'Wendy', 'William']


###############################################################################
###############################################################################
###############################################################################
class Player(object):
    def __init__(self, game, name='', quiet=False):
        self.game = game
        if not name:
            name = random.choice(playerNames)
        game.output("Player %s is at the table" % name)
        self.score = {}
        self.name = name
        self.messages = []
        self.hand = []
        self.deck = []
        # What cards have been played this turn
        self.played = []
        # Details for the current turn such as actions left, etc.
        self.t = {'buys': 1, 'actions': 1, 'gold': 0, 'potions': 0}
        self.turnstats = {'actions': 0, 'buys': 0}
        self.discardpile = []
        self.quiet = quiet
        self.test_input = []
        self.initial_Deck()
        self.pickUpHand()

    ###########################################################################
    def initial_Deck(self):
        """ Provide the initial deck - cards don't come from the piles
            hence add them back """
        self.game['Copper'].numcards += 7
        for i in range(7):
            self.deck.append(self.game['Copper'].remove())
        self.game['Estate'].numcards += 3
        for i in range(3):
            self.deck.append(self.game['Estate'].remove())
        random.shuffle(self.deck)

    ###########################################################################
    def output(self, msg, end='\n'):
        if not self.quiet:
            sys.stdout.write("%s: %s%s" % (self.name, msg, end))
        self.messages.append(msg)

    ###########################################################################
    def inHand(self, card):
        """ Return named card if card is in hand """
        for c in self.hand:
            if c.cardname == card.lower():
                return c
        return None

    ###########################################################################
    def trashCard(self, c):
        """ Take a card out of the game """
        c.hook_trashCard(game=self.game, player=self)
        self.game.trashpile.append(c)
        if c in self.played:
            self.played.remove(c)
        if c in self.hand:
            self.hand.remove(c)

    ###########################################################################
    def setPlayed(self, *cards):
        """ This is mostly used for testing """
        self.discardpile = []
        for c in cards:
            self.played.append(self.game[c].remove())

    ###########################################################################
    def setDiscard(self, *cards):
        """ This is mostly used for testing """
        self.discardpile = []
        for c in cards:
            self.discardpile.append(self.game[c].remove())

    ###########################################################################
    def setHand(self, *cards):
        """ This is mostly used for testing """
        self.hand = []
        for c in cards:
            self.hand.append(self.game[c].remove())

    ###########################################################################
    def setDeck(self, *cards):
        """ This is mostly used for testing """
        self.deck = []
        for c in cards:
            self.deck.append(self.game[c].remove())

    ###########################################################################
    def nextCard(self):
        """ Return the next card from the deck """
        if not self.deck:
            self.shuffleDeck()
            while self.discardpile:
                self.addCard(self.discardpile.pop(), 'deck')
        if not self.deck:
            self.output("No more cards in deck")
            return None
        c = self.deck.pop()
        return c

    ###########################################################################
    def pickupCard(self, card=None, verbose=True, verb='Picked up'):
        """ Pick a card from the deck and put it into the players hand """
        if not card:
            card = self.nextCard()
            if not card:
                self.output("No more cards to pickup")
                return None
        self.addCard(card, 'hand')
        if verbose:
            self.output("%s %s" % (verb, card.name))
        return card

    ###########################################################################
    def shuffleDeck(self):
        self.output("Shuffling Pile of %d cards" % len(self.discardpile))
        random.shuffle(self.discardpile)

    ###########################################################################
    def pickUpHand(self, handsize=5):
        while len(self.hand) < handsize:
            self.pickupCard(verb='Dealt')

    ###########################################################################
    def addCard(self, c, pile='discard'):
        if not c:
            return
        if pile == 'discard':
            self.discardpile.append(c)
        elif pile == 'hand':
            self.hand.append(c)
        elif pile == 'topdeck':
            self.deck.append(c)
        elif pile == 'deck':
            self.deck.insert(0, c)
        elif pile == 'played':
            self.played.append(c)

    ###########################################################################
    def discardCard(self, c):
        if c in self.hand:
            self.hand.remove(c)
        self.addCard(c, 'discard')

    ###########################################################################
    def discardHand(self):
        for c in self.hand + self.played:
            self.hook_discardCard(c)
        while self.hand:
            self.discardCard(self.hand.pop())
        while self.played:
            self.discardCard(self.played.pop())

    ###########################################################################
    def userInput(self, options, prompt):
        for o in options:
            self.output("%s)\t%s" % (o['selector'], o['print']))
        self.output(prompt, end=' ')
        while(1):
            if self.test_input:
                inp = self.test_input.pop(0)
            else:
                inp = raw_input()
            for o in options:
                if o['selector'] == inp:
                    return o
            self.output("Invalid Option (%s)" % inp)

    ###########################################################################
    def playableSelection(self, index):
        options = []
        playable = [c for c in self.hand if c.playable]
        for p in playable:
            sel = chr(ord('a')+index)
            pr = "Play %s (%s)" % (p.name, p.desc)
            options.append({'selector': sel, 'print': pr, 'card': p, 'action': 'play'})
            index += 1
        return options, index

    ###########################################################################
    def spendableSelection(self, index):
        options = []
        spendable = [c for c in self.hand if c.isTreasure()]
        if spendable:
            sel = chr(ord('a')+index)
            totgold = sum([self.hook_spendValue(c) for c in spendable])
            numpots = sum([1 for c in spendable if c.name == 'Potion'])
            potstr = ", %d potions" % numpots if numpots else ""
            tp = 'Spend all treasures (%d gold%s)' % (totgold, potstr)
            options.append({'selector': sel, 'print': tp, 'card': None, 'action': 'spendall'})
            index += 1
        for s in spendable:
            sel = chr(ord('a')+index)
            tp = 'Spend %s (%d gold)' % (s.name, self.hook_spendValue(s))
            options.append({'selector': sel, 'print': tp, 'card': s, 'action': 'spend'})
            index += 1

        for c in self.hand:
            if c.name == 'Potion':
                sel = chr(ord('a')+index)
                tp = 'Spend %s' % s.name
                options.append({'selector': sel, 'print': tp, 'card': s, 'action': 'spend'})
                index += 1
        return options, index

    ###########################################################################
    def buyableSelection(self, index):
        options = []
        buyable = self.cardsUnder(gold=self.t['gold'], potions=self.t['potions'])
        for p in buyable:
            if not self.hook_allowedToBuy(p):
                continue
            sel = chr(ord('a')+index)
            tp = 'Buy %s (%s) %s (%d left)' % (p.name, self.coststr(p), p.desc, p.numcards)
            options.append({'selector': sel, 'print': tp, 'card': p, 'action': 'buy'})
            index += 1
        return options, index

    ###########################################################################
    def choiceSelection(self):
        options = [{'selector': '0', 'print': 'End Turn', 'card': None, 'action': 'quit'}]
        index = 0

        if self.t['actions']:
            op, index = self.playableSelection(index)
            options.extend(op)

        if self.t['buys']:
            op, index = self.spendableSelection(index)
            options.extend(op)
            op, index = self.buyableSelection(index)
            options.extend(op)

        prompt = "What to do (actions=%(actions)d buys=%(buys)d gold=%(gold)d potions=%(potions)d)?" % self.t
        return self.userInput(options, prompt)

    ###########################################################################
    def addScore(self, reason, points):
        if reason not in self.score:
            self.score[reason] = 0
        self.score[reason] += points

    ###########################################################################
    def allCards(self):
        return self.discardpile + self.hand + self.deck + self.played

    ###########################################################################
    def getScoreDetails(self, verbose=False):
        scr = {}
        for c in self.allCards():
            scr[c.name] = scr.get(c.name, 0) + c.victory
            scr[c.name] = scr.get(c.name, 0) + c.special_score(self.game, self)
        scr.update(self.score)
        return scr

    ###########################################################################
    def getScore(self, verbose=False):
        scr = self.getScoreDetails(verbose)
        vp = sum(scr.values())
        if verbose:
            self.game.output("%s: %s" % (self.name, scr))
        return vp

    ###########################################################################
    def hook_allowedToBuy(self, card):
        """ Hook to check if you are allowed to buy a card """
        return card.hook_allowedToBuy(game=self.game, player=self)

    ###########################################################################
    def hook_buyCard(self, card):
        """ Hook for after purchasing a card """
        for c in self.hand:
            c.hook_buyCard(game=self.game, player=self, card=card)

    ###########################################################################
    def turn(self):
        self.played = []
        self.output("#" * 80)
        stats = "(%d points, %d cards)" % (self.getScore(), self.countCards())
        self.output("%s Turn %s" % (self.name, stats))
        self.t = {'buys': 1, 'actions': 1, 'gold': 0, 'potions': 0}
        self.turnstats = {'actions': 0, 'buys': 0}
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
                self.hook_buyCard(opt['card'])
            elif opt['action'] == 'play':
                self.turnstats['actions'] += 1
                self.playCard(opt['card'])
            elif opt['action'] == 'spend':
                self.spendCard(opt['card'])
            elif opt['action'] == 'spendall':
                self.spendAllCards()
            elif opt['action'] == 'quit':
                break
            else:
                sys.stderr.write("ERROR: Unhandled action %s" % opt['action'])
        self.discardHand()
        self.pickUpHand()

    ###########################################################################
    def spendCard(self, card):
        self.t['gold'] += self.hook_spendValue(card)
        self.t['potions'] += card.potion
        self.addCard(card, 'played')
        self.hand.remove(card)
        card.special(game=self.game, player=self)

    ###########################################################################
    def hook_discardCard(self, card):
        """ A card has been discarded """
        card.hook_discardCard(game=self.game, player=self)

    ###########################################################################
    def hook_spendValue(self, card):
        """ How much do you get for spending the card """
        val = card.hook_goldvalue(game=self.game, player=self)
        for c in self.played:
            val += c.hook_spendValue(game=self.game, player=self, card=card)
        return val

    ###########################################################################
    def spendAllCards(self):
        for card in self.hand[:]:
            if card.isTreasure():
                self.spendCard(card)

    ###########################################################################
    def playCard(self, card, discard=True, costAction=True):
        if discard:
            self.addCard(card, 'played')
            self.hand.remove(card)
        if costAction:
            self.t['actions'] -= 1
        self.t['actions'] += card.actions
        self.t['gold'] += card.gold
        self.t['buys'] += card.buys
        for i in range(card.cards):
            self.pickupCard()
        card.special(game=self.game, player=self)

    ###########################################################################
    def cardCost(self, card):
        cost = card.cost
        for c in self.hand + self.played:
            cost += c.hook_cardCost(game=self.game, player=self, card=card)
        return max(0, cost)

    ###########################################################################
    def gainCard(self, cardpile, destination='discard'):
        """ Add a new card to the players set of cards from a cardpile """
        if isinstance(cardpile, str):
            newcard = self.game[cardpile].remove()
        else:
            newcard = cardpile.remove()
        options = self.hook_gainCard(newcard)
        if not newcard:
            sys.stderr.write("ERROR: Getting from empty cardpile %s" % cardpile)
            return
        if 'destination' in options:
            destination = options['destination']
        self.addCard(newcard, destination)
        return newcard

    ###########################################################################
    def hook_purchasedCard(self, card):
        """ Hook which is fired when the card has been bought """
        card.hook_purchasedCard(game=self.game, player=self)

    ###########################################################################
    def buyCard(self, card):
        newcard = self.gainCard(card)
        self.t['buys'] -= 1
        self.t['gold'] -= self.cardCost(newcard)
        self.hook_purchasedCard(card)
        self.output("Bought %s for %d gold" % (newcard.name, self.cardCost(newcard)))

    ###########################################################################
    def hook_gainCard(self, card):
        """ Hook which is fired by a card being obtained by a player """
        options = {}
        for c in self.hand:
            o = c.hook_gainCard(game=self.game, player=self, card=card)
            options.update(o)
        return options

    ###########################################################################
    def hasDefense(self, attacker, verbose=True):
        for c in self.hand:
            c.hook_underAttack(game=self.game, player=self)
            if c.hasDefense():
                if verbose:
                    attacker.output("Player %s is defended" % self.name)
                return True
        return False

    ###########################################################################
    def plrTrashCard(self, printcost=False, force=False, exclude=[]):
        """ Ask player to trash a single card
            force - must trash a card, otherwise have option not to trash
            printcost - print the cost of the card being trashed
            exclude - can't select a card in the exclude list to be trashed
        """
        self.output("Trash a card")
        if force:
            options = []
        else:
            options = [{'selector': '0', 'print': 'Trash nothing', 'card': None}]

        index = 1
        for c in self.hand:
            if exclude and c.name in exclude:
                continue
            sel = "%d" % index
            if printcost:
                pr = "Trash %s (%d gold)" % (c.name, self.cardCost(c))
            else:
                pr = "Trash %s" % c.name
            options.append({'selector': sel, 'print': pr, 'card': c})
            index += 1
        o = self.userInput(options, "Trash which card?")
        if not o['card']:
            return
        trash = o['card']
        self.trashCard(trash)
        return trash

    ###########################################################################
    def cardsAffordable(self, oper, gold, potions=0, types={}):
        """Return the list of cards for under cost """
        affordable = []
        for c in self.game.cardTypes():
            cost = self.cardCost(c)
            if not c.purchasable:
                continue
            if c.isAction() and not types['action']:
                continue
            if c.isVictory() and not types['victory']:
                continue
            if c.isTreasure() and not types['treasure']:
                continue
            if not c.numcards:
                continue
            if oper(cost, gold) and oper(c.potcost, potions):
                affordable.append(c)
        affordable.sort(key=lambda c: self.cardCost(c))
        affordable.sort(key=lambda c: c.basecard)
        return affordable

    ###########################################################################
    def cardsUnder(self, gold, potions=0, types={}):
        """Return the list of cards for under cost """
        types = self.typeSelector(types)
        return self.cardsAffordable(operator.le, gold, potions, types)

    ###########################################################################
    def cardsWorth(self, gold, potions=0, types={}):
        """Return the list of cards that are exactly cost """
        types = self.typeSelector(types)
        return self.cardsAffordable(operator.eq, gold, potions, types)

    ###########################################################################
    def countCards(self):
        return len(self.allCards())

    ###########################################################################
    def typeSelector(self, types):
        if not types:
            return {'action': True, 'victory': True, 'treasure': True}
        _types = {'action': False, 'victory': False, 'treasure': False}
        _types.update(types)
        return _types

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
            selector = "%d" % index
            toprint = 'Get %s (%s) %s' % (p.name, self.coststr(p), p.desc)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1

        o = chooser.userInput(options, "What card do you wish?")
        if o['card']:
            self.addCard(o['card'].remove(), destination)
            return o['card']

    ###########################################################################
    def coststr(self, card):
        goldcost = "%d gold" % self.cardCost(card)
        potcost = "%d potions" % card.potcost if card.potcost else ""
        cststr = "%s %s" % (goldcost, potcost)
        return cststr.strip()

    ###########################################################################
    def plrDiscardCards(self, num):
        """ Get the player to discard exactly num cards """
        discard = []
        while(1):
            options = []
            if num == len(discard) or len(self.hand) == len(discard):
                options = [{'selector': '0', 'print': 'Finished selecting', 'card': None}]
            index = 1
            for c in self.hand:
                sel = "%s" % index
                pr = "%s %s" % ("Undiscard" if c in discard else "Discard", c.name)
                options.append({'selector': sel, 'print': pr, 'card': c})
                index += 1

            numleft = num - len(discard)
            o = self.userInput(options, "Discard %s more cards." % numleft)
            if o['card']:
                if o['card'] in discard:
                    discard.remove(o['card'])
                else:
                    discard.append(o['card'])
            if o['card'] is None:
                break
        for c in discard:
            self.discardCard(c)

    ###########################################################################
    def plrDiscardDownTo(self, num):
        """ Get the player to discard down to num cards in their hand """
        numtogo = len(self.hand) - num
        self.plrDiscardCards(numtogo)

#EOF

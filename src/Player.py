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
    def __init__(self, game, name=''):
        self.game = game
        if not name:
            name = random.choice(playerNames)
        game.output("Player %s is at the table" % name)
        self.basescore = 0
        self.name = name
        self.hand = []
        self.deck = []
        # Details for the current turn such as actions left, etc.
        self.t = {'buys': 1, 'actions': 1, 'gold': 0}
        self.turnstats = {'actions': 0, 'buys': 0}
        self.discardpile = []
        self.initial_Deck()

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
        self.pickUpHand()

    ###########################################################################
    def output(self, msg, end='\n'):
        sys.stdout.write("%s: %s%s" % (self.name, msg, end))

    ###########################################################################
    def trashCard(self, c):
        """ Take a card out of the game """
        # TODO: Need to prevent cards being trashed that have already been used to buy
        self.game.trashpile.append(c)
        self.t['gold'] -= c.gold
        if c in self.hand:
            self.hand.remove(c)

    ###########################################################################
    def nextCard(self):
        """ Return the next card from the deck """
        if not(self.deck):
            self.shuffleDeck()
            while self.discardpile:
                self.deck.append(self.discardpile.pop())
        if not self.deck:
            self.output("No more cards in deck")
            return None
        c = self.deck.pop()
        return c

    ###########################################################################
    def pickupCard(self, card=None, verbose=True):
        """ Pick a card from the deck and put it into the players hand """
        if not card:
            card = self.nextCard()
        self.addCard(card, 'hand')
        if verbose:
            self.output("Picked up %s" % card.name)
        return card

    ###########################################################################
    def shuffleDeck(self):
        random.shuffle(self.discardpile)

    ###########################################################################
    def pickUpHand(self, handsize=5):
        while len(self.hand) < handsize:
            self.pickupCard()

    ###########################################################################
    def addCard(self, c, pile='discard'):
        if not c:
            return
        if pile == 'discard':
            self.discardpile.append(c)
        elif pile == 'hand':
            self.hand.append(c)
            self.t['gold'] += c.gold
        elif pile == 'deck':
            self.deck.append(c)

    ###########################################################################
    def discardCard(self, c):
        self.hand.remove(c)
        self.addCard(c, 'discard')

    ###########################################################################
    def discardHand(self):
        for c in self.hand[:]:
            self.discardCard(c)

    ###########################################################################
    def userInput(self, options, prompt):
        for o in options:
            self.output("%s)\t%s" % (o['selector'], o['print']))
        self.output(prompt, end=' ')
        while(1):
            input = raw_input()
            for o in options:
                if o['selector'] == input:
                    return o
            self.output("Invalid Option (%s)" % input)

    ###########################################################################
    def choiceSelection(self):
        options = [{'selector': '0', 'print': 'End Turn', 'card': None, 'action': 'quit'}]
        index = 0

        if self.t['actions']:
            playable = [c for c in self.hand if c.playable]
            for p in playable:
                sel = chr(ord('a')+index)
                pr = "Play %s (%s)" % (p.name, p.desc)
                options.append({'selector': sel, 'print': pr, 'card': p, 'action': 'play'})
                index += 1

        if self.t['buys']:
            spendable = [c for c in self.hand if c.isTreasure()]
            if spendable:
                sel = chr(ord('a')+index)
                toprint = 'Spend all treasures (%d gold)' % sum([c.gold for c in spendable])
                options.append({'selector': sel, 'print': toprint, 'card': None, 'action': 'spendall'})
                index += 1
            for s in spendable:
                sel = chr(ord('a')+index)
                toprint = 'Spend %s (%d gold)' % (s.name, s.gold)
                options.append({'selector': sel, 'print': toprint, 'card': s, 'action': 'spend'})
                index += 1
            purchasable = self.game.cardsUnder(self.t['gold'])
            for p in purchasable:
                if not self.hook_allowedtobuy(p):
                    continue
                sel = chr(ord('a')+index)
                toprint = 'Buy %s (%d gold) %s (%d left)' % (p.name, p.cost, p.desc, p.numcards)
                options.append({'selector': sel, 'print': toprint, 'card': p, 'action': 'buy'})
                index += 1

        prompt = "What to do (actions=%(actions)d buys=%(buys)d gold=%(gold)d)?" % self.t
        return self.userInput(options, prompt)

    ###########################################################################
    def score(self):
        allcards = self.discardpile + self.hand + self.deck
        vp = sum([c.victory for c in allcards])
        vp += sum([c.special_score(self.game, self) for c in allcards])
        vp += self.basescore
        return vp

    ###########################################################################
    def hook_allowedtobuy(self, card):
        """ Hook to check if you are allowed to buy a card """
        return card.hook_allowedtobuy(game=self.game, player=self)

    ###########################################################################
    def hook_buycard(self, card):
        """ Hook for after purchasing a card """
        for c in self.hand:
            c.hook_buycard(game=self.game, player=self, card=card)

    ###########################################################################
    def turn(self):
        self.output("#" * 80)
        self.output("%s Turn (%d points)" % (self.name, self.score()))
        self.t = {'buys': 1, 'actions': 1, 'gold': 0}
        self.turnstats = {'actions': 0, 'buys': 0}
        while(1):
            if self.hand:
                self.output("Hand: %s" % ", ".join([c.name for c in self.hand]))
            else:
                self.output("Hand: <EMPTY>")
            opt = self.choiceSelection()
            if opt['action'] == 'buy':
                self.buyCard(opt['card'])
                self.hook_buycard(opt['card'])
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
        self.discardCard(card)
        self.t['gold'] += card.gold

    ###########################################################################
    def spendAllCards(self):
        for card in self.hand[:]:
            if card.isTreasure():
                self.discardCard(card)
                self.t['gold'] += card.gold

    ###########################################################################
    def playCard(self, card, discard=True, costAction=True):
        if discard:
            self.discardCard(card)
        if costAction:
            self.t['actions'] -= 1
        self.t['actions'] += card.actions
        self.t['gold'] += card.gold
        self.t['buys'] += card.buys
        for i in range(card.cards):
            c = self.pickupCard()
        card.special(game=self.game, player=self)

    ###########################################################################
    def gainCard(self, cardpile, destination='discard'):
        """ Add a new card to the players set of cards from a cardpile """
        if type(cardpile) == type(''):
            newcard = self.game[cardpile].remove()
        else:
            newcard = cardpile.remove()
        options = self.hook_gaincard(newcard)
        if not newcard:
            sys.stderr.write("ERROR: Getting from empty cardpile %s" % cardpile)
            return
        if 'destination' in options:
            destination = options['destination']
        self.addCard(newcard, destination)
        return newcard

    ###########################################################################
    def buyCard(self, card):
        newcard = self.gainCard(card)
        self.t['buys'] -= 1
        self.t['gold'] -= newcard.cost
        self.output("Bought %s for %d gold" % (newcard.name, newcard.cost))

    ###########################################################################
    def hook_gaincard(self, card):
        """ Hook which is fired by a card being obtained by a player """
        options = {}
        for c in self.hand:
            o = c.hook_gaincard(game=self.game, player=self, card=card)
            options.update(o)
        return options

    ###########################################################################
    def hasDefense(self, verbose=True):
        for c in self.hand:
            if c.hasDefense():
                if verbose:
                    self.output("Player %s is defended" % self.name)
                return True
        return False

    ###########################################################################
    def plrTrashCard(self, printcost=False):
        """ Ask player to trash a single card """
        self.output("Trash a card")
        options = [{'selector': '0', 'print': 'Trash nothing', 'card': None}]
        index = 1
        for c in self.hand:
            sel = "%d" % index
            if printcost:
                pr = "Trash %s (%d gold)" % (c.name, c.cost)
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
    def plrGainCard(self, cost, modifier='less'):
        """ Gain a card of players choice up to cost gold """
        options = [{'selector': '0', 'print': 'Nothing', 'card': None}]
        if modifier == 'less':
            self.output("Gain a card costing up to %d" % cost)
            purchasable = self.game.cardsUnder(cost)
        elif modifier == 'equal':
            self.output("Gain a card costing exactly %d" % cost)
            purchasable = self.game.cardsWorth(cost)
        else:
            self.output("Unhandled modifier: %s" % modifier)
        index = 1
        for p in purchasable:
            selector = "%d" % index
            toprint = 'Get %s (%d gold) %s' % (p.name, p.cost, p.desc)
            options.append({'selector': selector, 'print': toprint, 'card': p})
            index += 1

        o = self.userInput(options, "What card do you wish?")
        if o['card']:
            self.addCard(o['card'].remove())
            return o['card']

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

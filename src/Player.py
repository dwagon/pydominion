import random
import sys

playerNames = ['Adam', 'Alan', 'Alexander', 'Amanda', 'Amy', 'Andrew', 'Angela',
    'Anne', 'Anthony', 'Barbara', 'Benjamin', 'Brian', 'Catherine', 'Chloe',
    'Christine', 'Christopher', 'Colin', 'Craig', 'Daniel', 'Darren', 'David',
    'Elizabeth', 'Emily', 'Emma', 'Fiona', 'Gary', 'Geoffrey', 'George',
    'Graeme', 'Gregory', 'Heather', 'Helen', 'Ian', 'Jack', 'James', 'Jason',
    'Jennifer', 'Jessica', 'Joan', 'Joanne', 'John', 'Joshua', 'Judith',
    'Julie', 'Karen', 'Kate', 'Kathleen', 'Kenneth', 'Kevin', 'Lachlan',
    'Laura', 'Lauren', 'Leanne', 'Linda', 'Lisa', 'Luke', 'Lynette',
    'Margaret', 'Maria', 'Mark', 'Mary', 'Matthew', 'Melissa', 'Michael',
    'Michelle', 'Natalie', 'Nathan', 'Nicholas', 'Nicole', 'Olivia', 'Pamela',
    'Patricia', 'Paul', 'Peter', 'Raymond', 'Rebecca', 'Richard', 'Robert',
    'Robyn', 'Ronald', 'Ryan', 'Samantha', 'Samuel', 'Sandra', 'Sarah',
    'Scott', 'Shane', 'Sharon', 'Shirley', 'Simon', 'Stephanie', 'Stephen',
    'Steven', 'Susan', 'Suzanne', 'Thomas', 'Timothy', 'Wayne', 'Wendy',
    'William']


###############################################################################
###############################################################################
###############################################################################
class Player(object):
    def __init__(self, game, name=''):
        self.game = game
        if not name:
            name = random.choice(playerNames)
        self.name = name
        self.hand = []
        self.deck = []
        self.t = {'buys': 1, 'actions': 1, 'gold': 0}  # Details for the current turn such as actions left, etc.
        self.discardpile = []
        self.initial_Deck()

    ###########################################################################
    def initial_Deck(self):
        for i in range(7):
            self.deck.append(self.game['Copper'].remove())
        for i in range(3):
            self.deck.append(self.game['Estate'].remove())
        random.shuffle(self.deck)
        self.pickUpHand()

    ###########################################################################
    def trashCard(self, c):
        """ Take a card out of the game """
        # TODO: Need to prevent cards being trashed that have already been used to buy
        self.game.trashpile.append(c)
        self.t['gold'] -= c.gold
        self.hand.remove(c)

    ###########################################################################
    def pickupCard(self):
        """ Pick a card from the deck and put it into the players hand """
        if not(self.deck):
            self.shuffleDeck()
            while self.discardpile:
                self.deck.append(self.discardpile.pop())
        if not self.deck:
            print "No more cards in deck"
            return None
        c = self.deck.pop()
        self.hand.append(c)
        self.t['gold'] += c.gold
        return c

    ###########################################################################
    def shuffleDeck(self):
        random.shuffle(self.discardpile)

    ###########################################################################
    def pickUpHand(self):
        while len(self.hand) < 5:
            self.pickupCard()

    ###########################################################################
    def addCard(self, c, pile='discard'):
        if pile == 'discard':
            self.discardpile.append(c)
        elif pile == 'hand':
            self.hand.append(c)
        elif pile == 'deck':
            self.deck.insert(0, c)

    ###########################################################################
    def discardCard(self, c):
        self.hand.remove(c)
        self.addCard(c, 'discard')

    ###########################################################################
    def discardHand(self):
        for c in self.hand:
            self.discardCard(c)

    ###########################################################################
    def choiceSelection(self):
        options = [{'selector': '0', 'print': 'End Turn', 'card': None, 'action': 'quit'}]

        if self.t['actions']:
            index = 1
            playable = [c for c in self.hand if c.playable]
            for p in playable:
                selector = "%d" % index
                options.append({'selector': selector, 'print': 'Play %s' % p.name, 'card': p, 'action': 'play'})
                index += 1

        if self.t['buys']:
            index = 0
            purchasable = self.game.cardsUnder(self.t['gold'])
            for p in purchasable:
                selector = chr(ord('a')+index)
                toprint = 'Buy %s (%d gold)' % (p.name, p.cost)
                options.append({'selector': selector, 'print': toprint, 'card': p, 'action': 'buy'})
                index += 1

        for o in options:
            print "%s\t%s" % (o['selector'], o['print'])
        print "What to do (actions=%(actions)d buys=%(buys)d gold=%(gold)d)?" % self.t,
        while(1):
            input = raw_input()
            for o in options:
                if o['selector'] == input:
                    return o
            print "Invalid Option (%s) - '0' to end turn" % input

    ###########################################################################
    def score(self):
        vp = sum([c.victory for c in self.discardpile + self.hand + self.deck])
        return vp

    ###########################################################################
    def turn(self):
        print "#" * 80
        print "%s Turn (%d points)" % (self.name, self.score())
        print "%s" % ", ".join([c.name.title() for c in self.hand])
        self.t = {'buys': 1, 'actions': 1, 'gold': 0}
        self.t['gold'] = sum([c.gold for c in self.hand if c.isTreasure()])
        while self.t['actions'] + self.t['buys']:
            opt = self.choiceSelection()
            if opt['action'] == 'buy':
                self.buyCard(opt['card'])
            elif opt['action'] == 'play':
                self.playCard(opt['card'])
            elif opt['action'] == 'quit':
                break
            else:
                sys.stderr.write("ERROR: Unhandled action %s" % opt['action'])
        self.discardHand()
        self.pickUpHand()

    ###########################################################################
    def playCard(self, card):
        self.discardCard(card)
        self.t['actions'] -= 1
        self.t['actions'] += card.actions
        self.t['gold'] += card.gold
        self.t['buys'] += card.buys
        for i in range(card.cards):
            self.pickupCard()
        card.special(game=self.game, player=self)

    ###########################################################################
    def buyCard(self, cardpile):
        newcard = cardpile.remove()
        if not newcard:
            sys.stderr.write("ERROR: Buying from empty cardpile %s" % repr(cardpile))
        self.t['buys'] -= 1
        self.t['gold'] -= newcard.cost
        print "Bought %s for %d gold" % (newcard.name, newcard.cost)
        self.addCard(newcard)

    ###########################################################################
    def hasDefense(self):
        for c in self.hand:
            if c.hasDefense():
                return True
        return False

    ###########################################################################
    def __repr__(self):
        handstr = ", ".join([c.name for c in self.hand])
        return "Player %s: %s" % (self.name, handstr)

#EOF

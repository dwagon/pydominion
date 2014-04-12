import random

playerNames = ['Adam', 'Alan', 'Alexander', 'Amanda', 'Amy', 'Andrew', 'Angela',
    'Anne', 'Anthony', 'Barbara', 'Benjamin', 'Brian', 'Catherine',
    'Chloe', 'Christine', 'Christopher', 'Colin', 'Craig', 'Daniel',
    'Darren', 'David', 'Elizabeth', 'Emily', 'Emma', 'Fiona', 'Gary',
    'Geoffrey', 'George', 'Graeme', 'Gregory', 'Heather', 'Helen',
    'Ian', 'Jack', 'James', 'Jason', 'Jennifer', 'Jessica', 'Joan',
    'Joanne', 'John', 'Joshua', 'Judith', 'Julie', 'Karen', 'Kate',
    'Kathleen', 'Kenneth', 'Kevin', 'Lachlan', 'Laura', 'Lauren',
    'Leanne', 'Linda', 'Lisa', 'Luke', 'Lynette', 'Margaret', 'Maria',
    'Mark', 'Mary', 'Matthew', 'Melissa', 'Michael', 'Michelle',
    'Natalie', 'Nathan', 'Nicholas', 'Nicole', 'Olivia', 'Pamela',
    'Patricia', 'Paul', 'Peter', 'Raymond', 'Rebecca', 'Richard',
    'Robert', 'Robyn', 'Ronald', 'Ryan', 'Samantha', 'Samuel', 'Sandra',
    'Sarah', 'Scott', 'Shane', 'Sharon', 'Shirley', 'Simon', 'Stephanie',
    'Stephen', 'Steven', 'Susan', 'Suzanne', 'Thomas', 'Timothy',
    'Wayne', 'Wendy', 'William']

class Player(object):
    def __init__(self, game, name=''):
        self.game = game
        if not name:
            name = random.choice(playerNames)
        self.name = name
        self.hand = []
        self.deck = []
        self.discard = []
        self.initial_Deck()

    def initial_Deck(self):
        for i in range(7):
            self.deck.append(self.game.cardpiles['Copper'].remove())
        for i in range(3):
            self.deck.append(self.game.cardpiles['Estate'].remove())
        random.shuffle(self.deck)

    def pickUpHand(self):
        if len(self.deck)<5:
            random.shuffle(self.discard)
            while self.discard:
                self.deck.append(self.discard.pop())

        while len(self.hand)<5:
            self.hand.append(self.deck.pop())
        self.hand.sort(key=lambda c: c.name)

    def discardHand(self):
        while self.hand:
            self.discard.append(self.hand.pop())

    def turn(self):
        self.pickUpHand()
        print "%s Turn" % self.name
        buys = 1
        actions = 1
        gold = sum([c.gold for c in self.hand])
        for n,c in enumerate(self.hand, start=1):
            print "%d\t%s\t%s" % (n, c.name.title(), c.cardtype)
        print "Gold: %d" % gold
        print "Which card to play?"
        input = raw_input()
# Do card selection here
        self.discardHand()

    def __repr__(self):
        handstr = ", ".join([c.name for c in self.hand])
        return "Player %s: %s" % (self.name, handstr)

#EOF

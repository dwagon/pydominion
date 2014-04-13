class Card(object):
    def __init__(self):
        self.image = None
        self.buys = 0
        self.cardtype = 'unknown'
        self.playable = True
        self.defense = False
        self.needcurse = False
        self.actions = 0
        self.gold = 0
        self.cost = 0
        self.cards = 0
        self.victory = 0

    def special(self, game, player):
        pass

    def hasDefense(self):
        return self.defense

    def isTreasure(self):
        if self.cardtype == 'treasure':
            return True
        return False

#EOF

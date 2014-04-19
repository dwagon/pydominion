class Card(object):
    def __init__(self):
        self.image = None
        self.desc = "TODO"
        self.name = "TODO"
        self.basecard = False
        self.cost = -1
        self.cardtype = 'unknown'
        self.playable = True
        self.defense = False
        self.needcurse = False
        self.actions = 0
        self.buys = 0
        self.gold = 0
        self.cards = 0
        self.victory = 0
        self.image = self.getImageName()

    def getImageName(self):
        c = self.__class__.__name__
        c = c.replace('Card_','')
        return 'images/%s.jpg' % c.lower()

    def special(self, game, player):
        pass

    def hasDefense(self):
        return self.defense

    def isTreasure(self):
        if self.cardtype == 'treasure':
            return True
        return False

    def isVictory(self):
        if self.cardtype == 'victory':
            return True
        return False

    def special_score(self, game, player):
        return 0

    def hook_gaincard(self, game, player, card):
        pass

#EOF

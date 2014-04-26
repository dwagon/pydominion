class Card(object):
    def __init__(self):
        self.image = None
        self.desc = "TODO"
        self.name = "TODO"
        self.basecard = False
        self.cost = -1
        self.cardtype = 'unknown'
        self.purchasable = True
        self.playable = True
        self.defense = False
        self.needcurse = False
        self.needpotion = False
        self.actions = 0
        self.buys = 0
        self.gold = 0
        self.cards = 0
        self.victory = 0
        self.cardname = self.getCardName()
        self.image = self.getImageName()

    def getCardName(self):
        c = self.__class__.__name__
        c = c.replace('Card_', '')
        return c.lower()

    def getImageName(self):
        return 'images/%s.jpg' % self.cardname

    def special(self, game, player):
        pass

    def hasDefense(self):
        return self.defense

    def isTreasure(self):
        if self.cardtype == 'treasure':
            return True
        return False

    def isAction(self):
        if self.cardtype == 'action':
            return True
        return False

    def isVictory(self):
        if self.cardtype == 'victory':
            return True
        return False

    def special_score(self, game, player):
        return 0

    def hook_buycard(self, game, player, card):
        pass

    def hook_allowedtobuy(self, game, player):
        return True

    def hook_gaincard(self, game, player, card):
        return {}

    def hook_spendvalue(self, game, player, card):
        """ Does this card make any  modifications on the value of spending a card """
        return 0

#EOF

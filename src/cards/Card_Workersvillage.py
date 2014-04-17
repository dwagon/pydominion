from Card import Card


class Card_Workersvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "TODO"
        self.name = 'workersvillage'
        self.image = 'images/workersvillage.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF

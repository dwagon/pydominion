from Card import Card


class Card_Venture(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "TODO"
        self.name = 'venture'
        self.image = 'images/venture.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF

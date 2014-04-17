from Card import Card


class Card_Peddler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "TODO"
        self.name = 'pedler'
        self.image = 'images/pedler.jpg'
        self.cost = 4

    def special(self, game, player):
        pass


#EOF

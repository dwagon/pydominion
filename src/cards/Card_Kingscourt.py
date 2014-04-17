from Card import Card


class Card_Kingscourt(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Play action 3 times"
        self.name = 'kingscourt'
        self.image = 'images/kingscourt.jpg'
        self.cost = 7

    def special(self, game, player):
        pass


#EOF

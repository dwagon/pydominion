from Card import Card


class Card_Loan(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "Play with treasures"
        self.name = 'loan'
        self.image = 'images/loan.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF

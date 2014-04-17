from Card import Card


class Card_Hoard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "numcards / 10 VP"
        self.name = 'hoard'
        self.image = 'images/hoard.jpg'
        self.cost = 4

    def special(self, game, player):
        pass


#EOF

from Card import Card


class Card_Goons(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "numcards / 10 VP"
        self.name = 'goons'
        self.image = 'images/goons.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF

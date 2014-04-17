from Card import Card


class Card_Grandmarket(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "numcards / 10 VP"
        self.name = 'grandmarket'
        self.image = 'images/grandmarket.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF

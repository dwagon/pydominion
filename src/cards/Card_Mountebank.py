from Card import Card


class Card_Mountebank(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "numcards / 10 VP"
        self.name = 'mountebank'
        self.image = 'images/mountebank.jpg'
        self.cost = 4

    def special(self, game, player):
        pass

#EOF

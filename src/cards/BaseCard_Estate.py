from Card import Card

class Card_Estate(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.name = 'estate'
        self.image = 'images/estate.jpg'
        self.cost = 2
        self.victory = 1

#EOF

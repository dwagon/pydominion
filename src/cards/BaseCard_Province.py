from Card import Card

class Card_Province(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.name = 'province'
        self.image = 'images/province.jpg'
        self.cost = 8
        self.victory = 6

#EOF

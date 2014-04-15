from Card import Card


class Card_Woodcutter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'woodcutter'
        self.image = 'images/woodcutter.jpg'
        self.buys = 1
        self.gold = 2
        self.cost = 3

#EOF

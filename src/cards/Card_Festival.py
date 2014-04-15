from Card import Card


class Card_Festival(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'festival'
        self.image = 'images/festival.jpg'
        self.actions = 2
        self.buys = 1
        self.gold = 2
        self.cost = 5

#EOF

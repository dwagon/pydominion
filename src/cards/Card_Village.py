from Card import Card


class Card_Village(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'village'
        self.image = 'images/village.jpg'
        self.cards = 1
        self.actions = 2
        self.cost = 3

#EOF

from Card import Card


class Card_Laboratory(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 cards, +1 action"
        self.name = 'laboratory'
        self.image = 'images/laboratory.jpg'
        self.cards = 2
        self.actions = 1
        self.cost = 5

#EOF

from Card import Card


class Card_Smithy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+3 cards"
        self.name = 'Smithy'
        self.cards = 3
        self.cost = 4

#EOF

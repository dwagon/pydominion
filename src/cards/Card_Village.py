from Card import Card


class Card_Village(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 cards, +2 actions"
        self.name = 'Village'
        self.cards = 1
        self.actions = 2
        self.cost = 3

#EOF

from Card import Card


class Card_Bazaar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 cards, +2 action, +1 gold"
        self.name = 'Bazaar'
        self.cards = 1
        self.actions = 2
        self.gold = 1
        self.cost = 5

#EOF

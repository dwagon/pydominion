from Card import Card


class Card_Market(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 cards, +1 action, +1 gold, +1 buys"
        self.name = 'Market'
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.gold = 1
        self.cost = 5

#EOF

from Card import Card


class Card_Market(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.name = 'market'
        self.image = 'images/market.jpg'
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.gold = 1
        self.cost = 5

#EOF

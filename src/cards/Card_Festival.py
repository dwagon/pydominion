from Card import Card


class Card_Festival(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+2 actions, +1 buys, +2 gold"
        self.name = 'Festival'
        self.actions = 2
        self.buys = 1
        self.gold = 2
        self.cost = 5

#EOF

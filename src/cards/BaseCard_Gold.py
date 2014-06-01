from Card import Card


class Card_Gold(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'dominion'
        self.desc = "+3 gold"
        self.playable = False
        self.basecard = True
        self.name = 'Gold'
        self.gold = 3
        self.cost = 6

#EOF

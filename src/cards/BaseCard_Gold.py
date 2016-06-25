from Card import Card


class Card_Gold(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'dominion'
        self.desc = "+3 coin"
        self.playable = False
        self.basecard = True
        self.name = 'Gold'
        self.coin = 3
        self.cost = 6
        self.numcards = 30

# EOF

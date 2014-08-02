from Card import Card


class Card_Silver(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'dominion'
        self.desc = "+2 coin"
        self.playable = False
        self.basecard = True
        self.name = 'Silver'
        self.coin = 2
        self.cost = 3

#EOF

from Card import Card


class Card_Platinum(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+5 gold"
        self.name = 'Platinum'
        self.playable = False
        self.basecard = True
        self.gold = 5
        self.cost = 9

#EOF

from Card import Card


class Card_Copper(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.basecard = True
        self.playable = False
        self.desc = "+1 gold"
        self.name = 'Copper'
        self.gold = 1
        self.cost = 0

#EOF

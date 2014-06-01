from Card import Card


class Card_Curse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "-1 VP"
        self.basecard = True
        self.playable = False
        self.purchasable = False
        self.name = 'Curse'
        self.cost = 0
        self.victory = -1

#EOF

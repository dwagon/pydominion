from Card import Card


class Card_Province(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "6 VP"
        self.playable = False
        self.basecard = True
        self.name = 'Province'
        self.cost = 8
        self.victory = 6

#EOF

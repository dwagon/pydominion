from Card import Card


class Card_Estate(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.desc = "1 VP"
        self.playable = False
        self.basecard = True
        self.name = 'Estate'
        self.cost = 2
        self.victory = 1

#EOF

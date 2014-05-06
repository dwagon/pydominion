from Card import Card


class Card_Colony(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'prosperity'
        self.desc = "+10 VP"
        self.basecard = True
        self.name = 'Colony'
        self.playable = False
        self.cost = 11
        self.victory = 10


#EOF

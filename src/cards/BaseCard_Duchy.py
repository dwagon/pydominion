from Card import Card


class Card_Duchy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "3 VP"
        self.playable = False
        self.basecard = True
        self.name = 'Duchy'
        self.cost = 5
        self.victory = 3

#EOF

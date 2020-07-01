from Card import Card


class Card_Estate(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "1 VP"
        self.playable = False
        self.basecard = True
        self.name = 'Estate'
        self.cost = 2
        self.victory = 1

    def calc_numcards(self, game):
        if game.numplayers == 2:
            return 8
        return 12

# EOF

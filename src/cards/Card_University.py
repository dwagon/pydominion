from Card import Card


class Card_University(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "Gain an action card costing up to 5"
        self.name = 'University'
        self.cost = 2
        self.potcost = 1

    def special(self, game, player):
        """ Gain an action card costing up to 5"""
        player.plrGainCard(5, actiononly=True)

#EOF

from Card import Card


class Card_Workshop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "Gain a card costing up to 4"
        self.name = 'Workshop'
        self.cost = 3

    def special(self, game, player):
        """ Gain a card costing up to 4"""
        player.plrGainCard(4)

#EOF

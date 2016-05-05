#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Sirmartin(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'knight']
        self.base = 'darkages'
        self.name = "Sir Martin"
        self.buys = 2
        self.cost = 4

    def special(self, game, player):
        """ Each other player reveals the top 2 cards of his deck,
            trashes one of them costing from 3 to 6 and discards the
            rest. If a knight is trashed by this, trash this card """
        self.knight_special(game, player)

# EOF

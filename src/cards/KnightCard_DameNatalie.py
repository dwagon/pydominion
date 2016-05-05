#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Damenatalie(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'knight']
        self.base = 'darkages'
        self.name = "Dame Natalie"
        self.cost = 5

    def special(self, game, player):
        """ You may gain a card costing up to 3.
            Each other player reveals the top 2 cards of his deck,
            trashes one of them costing from 3 to 6 and discards the
            rest. If a knight is trashed by this, trash this card """
        player.plrGainCard(3)
        self.knight_special(game, player)

# EOF

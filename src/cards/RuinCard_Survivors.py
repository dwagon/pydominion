#!/usr/bin/env python

import Game
from Card import Card


###############################################################################
class Card_Survivors(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = Game.DARKAGES
        self.purchasable = False
        self.cost = 0
        self.desc = "Look at top 2 cards of deck. Discard or retain on deck"
        self.name = "Survivors"

    def special(self, game, player):
        """ Look at the top 2 cards of your deck. Discard them or
            put them back in any order """
        # TODO

# EOF

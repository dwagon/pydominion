#!/usr/bin/env python

import Game
from Card import Card


###############################################################################
class Card_Ruinedmarket(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = Game.DARKAGES
        self.name = "Ruined Market"
        self.desc = "+1 Buy"
        self.purchasable = False
        self.cost = 0
        self.buys = 1

# EOF

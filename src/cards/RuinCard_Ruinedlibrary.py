#!/usr/bin/env python

import Game
from Card import Card


###############################################################################
class Card_Ruinedlibrary(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = Game.DARKAGES
        self.desc = "+1 Card"
        self.purchasable = False
        self.cost = 0
        self.name = "Ruined Library"
        self.cards = 1

# EOF

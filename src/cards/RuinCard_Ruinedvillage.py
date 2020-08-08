#!/usr/bin/env python

import Game
from Card import Card


###############################################################################
class Card_Ruinedvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.RUIN]
        self.base = Game.DARKAGES
        self.name = "Ruined Village"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Action"
        self.actions = 1

# EOF

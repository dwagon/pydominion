#!/usr/bin/env python

import Game
from Card import Card


###############################################################################
class Card_Abandonedmine(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.RUIN]
        self.base = Game.DARKAGES
        self.name = "Abandoned Mine"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 coin"
        self.coin = 1

# EOF

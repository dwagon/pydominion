#!/usr/bin/env python

import Game
import Card


###############################################################################
class Card_Ruinedvillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RUIN]
        self.base = Game.DARKAGES
        self.name = "Ruined Village"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Action"
        self.actions = 1

# EOF

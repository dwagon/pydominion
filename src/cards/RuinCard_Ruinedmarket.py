#!/usr/bin/env python

import Game
import Card


###############################################################################
class Card_Ruinedmarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RUIN]
        self.base = Game.DARKAGES
        self.name = "Ruined Market"
        self.desc = "+1 Buy"
        self.purchasable = False
        self.cost = 0
        self.buys = 1

# EOF

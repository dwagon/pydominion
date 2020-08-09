#!/usr/bin/env python

import Game
import Card


###############################################################################
class Card_Ruinedlibrary(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.RUIN]
        self.base = Game.DARKAGES
        self.desc = "+1 Card"
        self.purchasable = False
        self.cost = 0
        self.name = "Ruined Library"
        self.cards = 1

# EOF

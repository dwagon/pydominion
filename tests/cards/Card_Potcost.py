#!/usr/bin/env python

from dominion import Card


###############################################################################
class Card_PotCost(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION]
        self.potcost = True
        self.name = "Pot Cost"
        self.base = Card.CardExpansion.TEST


# EOF

#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Ruinedvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = 'darkages'
        self.name = "Ruined Village"
        self.purchasable = False
        self.cost = 0
        self.card = "+1 Action"
        self.actions = 1

#EOF

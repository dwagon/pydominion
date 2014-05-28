#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Abandonedmine(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = 'darkages'
        self.name = "Abandoned Mine"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Gold"
        self.gold = 1

#EOF

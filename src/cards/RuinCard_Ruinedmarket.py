#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Ruinedmarket(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = 'darkages'
        self.name = "Ruined Market"
        self.buys = 1


#EOF

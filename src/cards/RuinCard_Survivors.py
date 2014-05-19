#!/usr/bin/env python

from Card import Card


###############################################################################
class Card_Survivors(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'ruin']
        self.base = 'darkages'
        self.name = "Survivors"

    def special(self, player, game):
        """ Look at the top 2 cards of your deck. Discard them or
            put them back in any order """
        # TODO
        pass


#EOF

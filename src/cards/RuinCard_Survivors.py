#!/usr/bin/env python

import Game
import Card


###############################################################################
class Card_Survivors(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RUIN]
        self.base = Game.DARKAGES
        self.purchasable = False
        self.cost = 0
        self.desc = "TODO: Look at top 2 cards of deck. Discard or retain on deck"
        self.name = "Survivors"

    def special(self, game, player):
        """ Look at the top 2 cards of your deck. Discard them or
            put them back in any order """
        # TODO
        player.output("Not implemented yet")

# EOF

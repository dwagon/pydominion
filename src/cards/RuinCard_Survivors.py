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
        self.desc = "Look at the top 2 cards of your deck. Discard them or put them back in any order."
        self.name = "Survivors"

    def special(self, game, player):
        """ Look at the top 2 cards of your deck. Discard them or
            put them back in any order """
        crds = player.pickupCards(2)
        ans = player.plrChooseOptions(
            "What to do with survivors?",
            ("Discard {} and {}".format(crds[0].name, crds[1].name), 'discard'),
            ("Return {} and {} to deck".format(crds[0].name, crds[1].name), 'return')
        )
        if ans == 'discard':
            player.discardCard(crds[0])
            player.discardCard(crds[1])
        else:
            player.addCard(crds[0], 'deck')
            player.addCard(crds[1], 'deck')

# EOF

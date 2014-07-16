#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Rebuild(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "+1 action. Reveal cards from deck until victory"
        self.name = 'Rebuild'
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """ Name a card. Reveal cards from the top of your deck
            until you reveal a Victory card that is not the named card.
            Discard the other cards. Trash the Vcitory card and gain a
            Victory card cost up to 3 more than it"""
        player.output("Trash a card from your hand. Gain a card costing exactly 1 more than it")
        tc = player.plrTrashCard(printcost=True)
        if tc:
            cost = player.cardCost(tc[0], modifier='equal')
            player.plrGainCard(cost + 3)


###############################################################################
class Test_XXX(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['xxx'])
        self.g.startGame()
        self.plr = self.g.players[0]


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

#!/usr/bin/env python

import unittest
from Card import Card


class Card_Expand(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Trash a card from hand and gain one costing 3 more"
        self.name = 'Expand'
        self.cost = 7

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to
            3 more than the trashed card """
        tc = player.plrTrashCard(printcost=True, prompt="Trash a card from your hand. Gain another costing up to 3 more than the one you trashed")
        if tc:
            cost = tc[0].cost
            player.plrGainCard(cost + 3)


###############################################################################
class Test_Expand(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Expand'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.expand = self.g['Expand'].remove()

    def test_play(self):
        self.plr.setHand('Copper')
        self.plr.addCard(self.expand, 'hand')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.expand)
        self.assertTrue(self.plr.hand.isEmpty())
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertLessEqual(self.plr.discardpile[0].cost, 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

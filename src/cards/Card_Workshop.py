#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Workshop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DOMINION
        self.desc = "Gain a card costing up to 4"
        self.name = 'Workshop'
        self.cost = 3

    def special(self, game, player):
        """ Gain a card costing up to 4"""
        player.plrGainCard(4)


###############################################################################
class Test_Workshop(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Workshop', 'Feast'], badcards=['Blessed Village', 'Cemetery'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.wcard = self.g['Workshop'].remove()
        self.plr.addCard(self.wcard, 'hand')

    def test_gainzero(self):
        self.plr.test_input = ['Finish']
        self.plr.playCard(self.wcard)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discard_size(), 0)

    def test_gainone(self):
        self.plr.test_input = ['Get Feast']
        self.plr.playCard(self.wcard)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.discard_size(), 1)
        self.assertLessEqual(self.plr.discardpile[0].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

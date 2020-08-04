#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Armory(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "Gain a card costing up to 4 putting it on top of your deck"
        self.name = 'Armory'
        self.cost = 4

    def special(self, game, player):
        """ Gain a card costing up to 4"""
        player.plrGainCard(4, destination='deck')


###############################################################################
class Test_Armory(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Armory', 'Feast'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.armory = self.g['Armory'].remove()
        self.plr.addCard(self.armory, 'hand')

    def test_gainzero(self):
        self.plr.test_input = ['finish']
        self.plr.playCard(self.armory)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertTrue(self.plr.discardpile.is_empty())

    def test_gainone(self):
        self.plr.test_input = ['Feast']
        self.plr.deck.empty()
        self.plr.playCard(self.armory)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertLessEqual(self.plr.deck[-1].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

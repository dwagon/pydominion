#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Workshop(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Gain a card costing up to 4"
        self.name = 'Workshop'
        self.cost = 3

    def special(self, game, player):
        """ Gain a card costing up to 4"""
        player.plrGainCard(4)


###############################################################################
class Test_Workshop(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['workshop', 'feast'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.wcard = self.g['workshop'].remove()
        self.plr.addCard(self.wcard, 'hand')

    def test_gainzero(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.wcard)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardSize(), 0)

    def test_gainone(self):
        self.plr.test_input = ['1']
        self.plr.playCard(self.wcard)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardSize(), 1)
        self.assertLessEqual(self.plr.discardpile[0].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

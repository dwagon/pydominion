#!/usr/bin/env python

import unittest
from Card import Card


class Card_Altar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = "Gain a card costing up to 5"
        self.name = 'Altar'
        self.cost = 6

    def special(self, game, player):
        """ Gain a card costing up to 5"""
        player.plrGainCard(5)


###############################################################################
class Test_Altar(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Altar', 'Upgrade'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.altar = self.g['Altar'].remove()
        self.plr.addCard(self.altar, 'hand')

    def test_gainzero(self):
        self.plr.test_input = ['finish']
        self.plr.playCard(self.altar)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertTrue(self.plr.discardpile.isEmpty())

    def test_gainone(self):
        self.plr.test_input = ['get upgrade']
        self.plr.playCard(self.altar)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardSize(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Upgrade'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
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
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['armory', 'feast'])
        self.plr = self.g.players.values()[0]
        self.armory = self.g['armory'].remove()
        self.plr.addCard(self.armory, 'hand')

    def test_gainzero(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.armory)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardpile, [])

    def test_gainone(self):
        self.plr.test_input = ['1']
        self.plr.deck = []
        self.plr.playCard(self.armory)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardpile, [])
        self.assertLessEqual(self.plr.deck[-1].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

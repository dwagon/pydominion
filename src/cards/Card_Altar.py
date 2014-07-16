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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['altar', 'upgrade'])
        self.plr = self.g.playerList(0)
        self.altar = self.g['altar'].remove()
        self.plr.addCard(self.altar, 'hand')

    def test_gainzero(self):
        self.plr.test_input = ['nothing']
        self.plr.playCard(self.altar)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardpile, [])

    def test_gainone(self):
        self.plr.test_input = ['get upgrade']
        self.plr.playCard(self.altar)
        self.assertEquals(self.plr.handSize(), 5)
        self.assertEquals(self.plr.discardSize(), 1)
        self.assertLessEqual(self.plr.discardpile[0].name, 'Upgrade')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

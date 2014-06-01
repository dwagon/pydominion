#!/usr/bin/env python

import unittest
from Card import Card


class Card_University(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'alchemy'
        self.desc = "Gain an action card costing up to 5"
        self.name = 'University'
        self.cost = 2
        self.potcost = 1

    def special(self, game, player):
        """ Gain an action card costing up to 5"""
        c = player.plrGainCard(5, types={'action': True})
        if c:
            player.output("Gained %s from university" % c.name)


###############################################################################
class Test_University(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['university'])
        self.plr = self.g.players[0]
        self.university = self.g['university'].remove()
        self.plr.addCard(self.university, 'hand')

    def test_gain(self):
        self.plr.test_input = ['1']
        self.plr.playCard(self.university)
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertTrue(self.plr.discardpile[0].isAction())
        self.assertLessEqual(self.plr.discardpile[0].cost, 5)

    def test_none(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.university)
        self.assertEqual(self.plr.discardpile, [])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

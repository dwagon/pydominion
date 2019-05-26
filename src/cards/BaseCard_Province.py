#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Province(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "6 VP"
        self.playable = False
        self.basecard = True
        self.name = 'Province'
        self.cost = 8
        self.victory = 6

    def numcards(self, game):
        if game.numplayers == 2:
            return 8
        if game.numplayers > 4:
            return 3 * game.numplayers
        return 12


###############################################################################
class Test_Province(unittest.TestCase):
    def setUp(self):
        pass

    def test_two_player(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2)
        self.g.startGame()
        self.assertEqual(self.g['Province'].numcards, 8)
        self.plr = self.g.playerList()[0]

    def Xtest_five(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=5)
        self.g.startGame()
        self.assertEqual(self.g['Province'].numcards, 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

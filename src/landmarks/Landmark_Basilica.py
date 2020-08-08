#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Basilica(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Basilica"

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def desc(self, player):
        if self._vp <= 0:
            return "No effect"
        return "When you buy a card, if you have 2 Coin or more left, take 2VP from here. (%d VP left)" % self._vp

    def hook_buyCard(self, game, player, card):
        if self._vp <= 0:
            return
        if player.coin >= 2:
            player.output("Gained 2 VP from Basilica")
            self._vp -= 2
            player.addScore('Basilica', 2)


###############################################################################
class Test_Basilica(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Basilica'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """ Use Basilica """
        self.plr.coin = 4
        self.plr.buyCard(self.g['Copper'])
        self.assertEqual(self.plr.getScoreDetails()['Basilica'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

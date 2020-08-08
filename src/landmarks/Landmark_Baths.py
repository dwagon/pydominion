#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Baths(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Baths"

    def desc(self, player):
        return "When you end your turn without having gained a card, take 2VP from here. (%d left)" % self._vp

    def hook_end_turn(self, game, player):
        if not player.stats['gained']:
            player.output("Gaining 2 from Baths as no cards gained")
            player.addScore('Baths', 2)
            self._vp -= 2

    def setup(self, game):
        self._vp = 6 * game.numplayers


###############################################################################
class Test_Baths(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Baths'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_use(self):
        """ Use Baths """
        self.plr.coin = 4
        self.plr.end_turn()
        self.assertEqual(self.plr.getScoreDetails()['Baths'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

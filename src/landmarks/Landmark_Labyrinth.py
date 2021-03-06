#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Labyrinth(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Labyrinth"

    def desc(self, player):
        return "When you gain a 2nd card in one of your turns, take 2VP from here ({} left)".format(self._vp)

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_gain_card(self, game, player, card):
        if len(player.stats['gained']) == 1:    # not including the current one
            player.addScore('Labyrinth', 2)
            player.output("Gained 2VP from Labyrinth")
            self._vp -= 2


###############################################################################
class Test_Labyrinth(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Labyrinth'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """ Use Labyrinth """
        self.assertNotIn('Labyrinth', self.plr.getScoreDetails())
        self.plr.gainCard('Copper')
        self.assertNotIn('Labyrinth', self.plr.getScoreDetails())
        self.plr.gainCard('Estate')
        self.assertEqual(self.plr.getScoreDetails()['Labyrinth'], 2)
        self.plr.gainCard('Gold')
        self.assertEqual(self.plr.getScoreDetails()['Labyrinth'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Labyrinth(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.name = "Labyrinth"

    def desc(self, player):
        return "When you gain a 2nd card in one of your turns, take 2VP from here ({} left)".format(self._vp)

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_gainCard(self, game, player, card):
        if len(player.stats['gained']) == 1:    # not including the current one
            player.addScore('Labyrinth', 2)
            player.output("Gained 2VP from Labyrinth")
            self._vp -= 2


###############################################################################
class Test_Labyrinth(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Labyrinth'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

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

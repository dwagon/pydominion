#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Wall(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When scoring, -1VP per card you have after the first 15."""
        self.name = "Wall"

    def hook_end_of_game(self, game, player):
        ncards = len(player.allCards())
        score = -(ncards - 15)
        player.addScore('Wall', score)


###############################################################################
class Test_Wall(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Wall'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """ Use Wall """
        self.plr.setDiscard('Gold', 'Silver', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.setDeck('Gold', 'Silver', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.setHand('Gold', 'Silver', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Wall'], -3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

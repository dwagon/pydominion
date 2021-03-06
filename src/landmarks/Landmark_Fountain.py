#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_Fountain(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "When scoring, 15VP if you have at least 10 Coppers."
        self.name = "Fountain"

    def hook_end_of_game(self, game, player):
        numcu = sum([1 for c in player.allCards() if c.name == 'Copper'])
        if numcu >= 10:
            player.addScore('Fountain', 15)
            player.output("Gained 15VP from Fountain")


###############################################################################
class Test_Fountain(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Fountain'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """ Use Fountain """
        self.plr.setDiscard('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.setDeck('Copper', 'Copper', 'Copper', 'Copper', 'Copper', 'Duchy')
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()['Fountain'], 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

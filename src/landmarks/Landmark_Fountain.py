#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Fountain(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = "When scoring, 15VP if you have at least 10 Coppers."
        self.name = "Fountain"

    def hook_end_of_game(self, game, player):
        numcu = sum([1 for c in player.allCards() if c.name == 'Copper'])
        if numcu >= 10:
            player.addScore('Fountain', 15)


###############################################################################
class Test_Fountain(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Fountain'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

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

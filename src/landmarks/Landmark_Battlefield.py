#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Battlefield(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = "When you gain a Victory card, take 2VP from here."
        self.name = "Battlefield"

    def hook_gainCard(self, game, player, card):
        if card.isVictory() and self._vp >= 0:
            self._vp -= 2
            player.addScore('Battlefield', 2)

    def setup(self, game):
        self._vp = 6 * game.numplayers


###############################################################################
class Test_Battlefield(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Battlefield'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_gain(self):
        """ Use Battlefield """
        self.plr.buyCard(self.g['Duchy'])
        self.assertEqual(self.plr.getScoreDetails()['Battlefield'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
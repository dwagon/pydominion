#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Baths(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.name = "Baths"
        self.desc = "When you end your turn without having gained a card, take 2VP from here."

    def hook_endTurn(self, game, player):
        if not player.stats['gained']:
            player.output("Gaining 2 from Baths as no cards gained")
            player.addScore('Baths', 2)

    def setup(self, game):
        self._vp = 6 * game.numplayers


###############################################################################
class Test_Baths(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Baths'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_use(self):
        """ Use Baths """
        self.plr.coin = 4
        self.plr.endTurn()
        self.assertEqual(self.plr.getScoreDetails()['Baths'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from Landmark import Landmark


###############################################################################
class Landmark_Tomb(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = 'empires'
        self.desc = """When you trash a card, +1VP"""
        self.name = "Tomb"

    def hook_trashCard(self, game, player, card):
        player.output("Gained 1 VP from Tomb")
        player.addScore('Tomb', 1)


###############################################################################
class Test_Tomb(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=['Tomb'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]

    def test_trash(self):
        """ Test Tomb"""
        cu = self.plr.inHand('Copper')
        self.plr.trashCard(cu)
        self.assertEqual(self.plr.getScoreDetails()['Tomb'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from Artifact import Artifact


###############################################################################
class Artifact_TreasureChest(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.cardtype = 'artifact'
        self.base = 'renaissance'
        self.desc = "At the start of your Buy phase, gain a Gold."
        self.name = "Treasure Chest"

    def hook_preBuy(self, game, player):
        player.gainCard("Gold")


###############################################################################
class Test_TreasureChest(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=['Treasure Chest'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_treasurechest(self):
        self.plr.assign_artifact('Treasure Chest')
        self.plr.test_input = ['End Phase']
        self.plr.buyPhase()
        self.assertIsNotNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

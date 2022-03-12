#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Artifact


###############################################################################
class Artifact_TreasureChest(Artifact.Artifact):
    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "At the start of your Buy phase, gain a Gold."
        self.name = "Treasure Chest"

    def hook_preBuy(self, game, player):
        player.gainCard("Gold")
        player.output("Gained a Gold from Treasure Chest")


###############################################################################
class Test_TreasureChest(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=["Treasure Chest"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_treasurechest(self):
        self.plr.assign_artifact("Treasure Chest")
        self.plr.test_input = ["End Phase"]
        self.plr.buy_phase()
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
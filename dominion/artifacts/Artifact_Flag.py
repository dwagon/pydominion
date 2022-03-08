#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Artifact


###############################################################################
class Artifact_Flag(Artifact.Artifact):
    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "When drawing your hand, +1 Card"
        self.name = "Flag"

    def hook_cleanup(self, game, player):
        player.newhandsize += 1


###############################################################################
class Test_Flag(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=["Flag"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.artifact = self.g.artifacts["Flag"]

    def test_flag(self):
        self.plr.assign_artifact("Flag")
        self.plr.end_turn()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

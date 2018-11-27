#!/usr/bin/env python

import unittest
from Artifact import Artifact


###############################################################################
class Artifact_Flag(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.cardtype = 'artifact'
        self.base = 'renaissance'
        self.desc = "When drawing your hand, +1 Card"
        self.name = "Flag"

    def hook_cleanup(self, game, player):
        player.newhandsize += 1


###############################################################################
class Test_Flag(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=['Flag'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.artifact = self.g.artifacts['Flag']

    def test_flag(self):
        self.plr.assign_artifact('Flag')
        self.plr.endTurn()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import Game
from Artifact import Artifact


###############################################################################
class Artifact_Key(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.cardtype = 'artifact'
        self.base = Game.RENAISSANCE
        self.desc = "At the start of your turn, +1 Coin."
        self.name = "Key"

    def hook_start_turn(self, game, player):
        player.addCoin(1)


###############################################################################
class Test_Key(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=['Key'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.artifact = self.g.artifacts['Key']

    def test_flag(self):
        self.plr.assign_artifact('Key')
        self.plr.start_turn()
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

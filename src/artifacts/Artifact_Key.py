#!/usr/bin/env python

import unittest
from Artifact import Artifact


###############################################################################
class Artifact_Key(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.cardtype = 'artifact'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, +1 Coin."
        self.name = "Key"

    def hook_startTurn(self, game, player):
        player.addCoin(1)


###############################################################################
class Test_Key(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=['Key'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.artifact = self.g.artifacts['Key']

    def test_flag(self):
        self.plr.assign_artifact('Key')
        self.plr.startTurn()
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import Game, Piles
from dominion import Artifact


###############################################################################
class Artifact_Key(Artifact.Artifact):
    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, +1 Coin."
        self.name = "Key"

    def hook_start_turn(self, game, player):
        player.coins.add(1)


###############################################################################
class Test_Key(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initartifacts=["Key"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.artifact = self.g.artifacts["Key"]

    def test_flag(self):
        self.plr.assign_artifact("Key")
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

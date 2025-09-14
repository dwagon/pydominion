#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Artifact, Card, Game, Player, OptionKeys


###############################################################################
class Artifact_Flag(Artifact.Artifact):
    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When drawing your hand, +1 Card"
        self.name = "Flag"

    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        player.newhandsize += 1
        return {}


###############################################################################
class Test_Flag(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initartifacts=["Flag"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.artifact = self.g.artifacts["Flag"]

    def test_flag(self) -> None:
        self.plr.assign_artifact("Flag")
        self.plr.end_turn()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

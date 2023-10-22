#!/usr/bin/env python

import unittest
from dominion import Card
from dominion import Game, Piles
from dominion import Artifact


###############################################################################
class Artifact_TreasureChest(Artifact.Artifact):
    def __init__(self):
        Artifact.Artifact.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your Buy phase, gain a Gold."
        self.name = "Treasure Chest"

    def hook_pre_buy(self, game, player):
        player.gain_card("Gold")
        player.output("Gained a Gold from Treasure Chest")


###############################################################################
class Test_TreasureChest(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initartifacts=["Treasure Chest"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_treasurechest(self):
        self.plr.assign_artifact("Treasure Chest")
        self.plr.test_input = ["End Phase"]
        self.plr.buy_phase()
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Gold"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_Cathedral(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, trash a card from your hand."
        self.name = "Cathedral"
        self.cost = 3

    def hook_start_turn(self, game, player):
        player.plr_trash_card(
            num=1, force=True, prompt="Cathedral forces you to trash a card"
        )


###############################################################################
class Test_Cathedral(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Cathedral"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.assign_project("Cathedral")
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Province")
        self.plr.test_input = ["Copper"]
        self.plr.start_turn()
        self.assertIn("Copper", self.g.trash_pile)
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

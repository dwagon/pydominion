#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_Sewers(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "When you trash a card other than with this, you may trash a card from your hand."
        self.name = "Sewers"
        self.cost = 3

    def hook_trash_card(self, game, player, card):
        player.plr_trash_card(prompt="Trash a card via Sewer", exclude_hook="Sewers")


###############################################################################
class Test_Sewers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initprojects=["Sewers"], initcards=["Chapel"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Chapel"].remove()

    def test_play(self):
        self.plr.set_hand("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.assign_project("Sewers")
        self.plr.test_input = ["Trash Copper", "Finish", "Trash Silver", "Finish"]
        self.plr.play_card(self.card)
        self.g.print_state()
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIsNotNone(self.g.in_trash("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

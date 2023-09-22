#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_Sewers(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When you trash a card other than with this, you may trash a card from your hand."
        self.name = "Sewers"
        self.cost = 3

    def hook_trash_card(self, game, player, card):
        player.plr_trash_card(prompt="Trash a card via Sewer", exclude_hook="Sewers")


###############################################################################
class TestSewers(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initprojects=["Sewers"], initcards=["Chapel"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Chapel")

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.assign_project("Sewers")
        self.plr.test_input = ["Trash Copper", "Finish", "Trash Silver", "Finish"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.g.trash_pile)
        self.assertIn("Silver", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

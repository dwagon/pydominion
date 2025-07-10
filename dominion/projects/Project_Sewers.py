#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Piles, Project, Player, OptionKeys


###############################################################################
class Project_Sewers(Project.Project):
    def __init__(self) -> None:
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When you trash a card other than with this, you may trash a card from your hand."
        self.name = "Sewers"
        self.cost = 3

    def hook_trash_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        player.plr_trash_card(prompt="Trash a card via Sewer", exclude_hook="Sewers")
        return {}


###############################################################################
class TestSewers(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, projects=["Sewers"], initcards=["Chapel"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Chapel")

    def test_play(self) -> None:
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

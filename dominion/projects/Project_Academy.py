#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Project, Player, OptionKeys


###############################################################################
class Project_Academy(Project.Project):
    def __init__(self) -> None:
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When you gain an Action card, +1 Villager."
        self.name = "Academy"
        self.cost = 5

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if card.isAction():
            player.output("Gained a villager from Academy")
            player.villagers += 1
        return {}


###############################################################################
class Test_Academy(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, projects=["Academy"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_have(self) -> None:
        self.assertEqual(self.plr.villagers.get(), 0)
        self.plr.assign_project("Academy")
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.villagers.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

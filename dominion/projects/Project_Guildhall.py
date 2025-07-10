#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Project, Player, OptionKeys


###############################################################################
class Project_Guildhall(Project.Project):
    def __init__(self) -> None:
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "When you gain a Treasure, +1 Coffers."
        self.name = "Guildhall"
        self.cost = 5

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if card.isTreasure():
            player.coffers.add(1)
        return {}


###############################################################################
class Test_Guildhall(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, projects=["Guildhall"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        numc = self.plr.coffers.get()
        self.plr.assign_project("Guildhall")
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.coffers.get(), numc + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

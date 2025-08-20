#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Exploration"""
import unittest

from dominion import Card, Game, Project


###############################################################################
class Project_Exploration(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = (
            """At the end of your Buy phase, if you didn't gain any cards during it, +1 Coffers and +1 Villager."""
        )
        self.name = "Exploration"
        self.cost = 4

    def hook_end_buy_phase(self, game, player):
        if player.stats["gained"]:
            return
        player.coffers.add(1)
        player.villagers += 1


###############################################################################
class TestExploration(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Exploration"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        num_coffers = self.plr.coffers.get()
        self.plr.assign_project("Exploration")
        self.plr.test_input = ["End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.coffers.get(), num_coffers + 1)
        self.assertEqual(self.plr.villagers.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Card, Game, Project


###############################################################################
class Project_Pageant(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the end of your Buy phase, you may pay 1 Coin for +1 Coffers."
        self.name = "Pageant"
        self.cost = 3

    def hook_end_buy_phase(self, game, player):
        options = []
        if not player.coins:
            return
        for num in range(player.coins.get() + 1):
            options.append((f"Buy {num} Coffers for {num} Coin", num))
        pick = player.plr_choose_options("Exchange coin for coffers", *options)
        player.coffers.add(pick)
        player.coins -= pick


###############################################################################
class TestPageant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Pageant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        num_coffers = self.plr.coffers.get()
        self.plr.assign_project("Pageant")
        self.plr.coins.set(5)
        self.plr.test_input = ["End Phase", "4"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.coffers.get(), num_coffers + 4)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

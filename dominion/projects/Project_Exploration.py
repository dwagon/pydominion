#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_Exploration(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "At the end of your Buy phase, if you didn't buy any cards, +1 Coffers and +1 Villager."
        self.name = "Exploration"
        self.cost = 4

    def hook_end_buy_phase(self, game, player):
        if player.stats["bought"]:
            return
        player.add_coffer(1)
        player.add_villager(1)


###############################################################################
class Test_Exploration(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Exploration"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        numc = self.plr.get_coffers()
        self.plr.assign_project("Exploration")
        self.plr.test_input = ["End Phase"]
        self.plr.buy_phase()
        self.assertEqual(self.plr.get_coffers(), numc + 1)
        self.assertEqual(self.plr.get_villagers(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

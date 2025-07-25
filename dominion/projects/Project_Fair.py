#!/usr/bin/env python

import unittest

from dominion import Card, Game, Project


###############################################################################
class Project_Fair(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, +1 Buy."
        self.name = "Fair"
        self.cost = 4

    def hook_start_turn(self, game, player):
        player.buys.add(1)


###############################################################################
class Test_Fair(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Fair"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        self.plr.assign_project("Fair")
        self.plr.start_turn()
        self.assertEqual(self.plr.buys.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

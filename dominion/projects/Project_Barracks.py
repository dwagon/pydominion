#!/usr/bin/env python

import unittest

from dominion import Card, Game, Project


###############################################################################
class Project_Barracks(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "At the start of your turn, +1 Action."
        self.name = "Barracks"
        self.cost = 6

    def hook_start_turn(self, game, player):
        player.add_actions(1)


###############################################################################
class Test_Barracks(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Barracks"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_flag(self):
        self.plr.assign_project("Barracks")
        self.plr.start_turn()
        self.assertEqual(self.plr.actions.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

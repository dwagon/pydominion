#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Barracks(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = Card.PROJECT
        self.base = Game.RENAISSANCE
        self.desc = "At the start of your turn, +1 Action."
        self.name = "Barracks"
        self.cost = 6

    def hook_start_turn(self, game, player):
        player.addActions(1)


###############################################################################
class Test_Barracks(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Barracks'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_flag(self):
        self.plr.assign_project('Barracks')
        self.plr.start_turn()
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

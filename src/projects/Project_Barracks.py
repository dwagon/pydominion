#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Barracks(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, +1 Action."
        self.name = "Barracks"
        self.cost = 6

    def hook_startTurn(self, game, player):
        player.addActions(1)


###############################################################################
class Test_Barracks(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Barracks'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_flag(self):
        self.plr.assign_project('Barracks')
        self.plr.startTurn()
        self.assertEqual(self.plr.getActions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

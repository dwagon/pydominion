#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Fair(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, +1 Buy."
        self.name = "Fair"
        self.cost = 4

    def hook_startTurn(self, game, player):
        player.addBuys(1)


###############################################################################
class Test_Fair(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Fair'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_play(self):
        self.plr.assign_project('Fair')
        self.plr.startTurn()
        self.assertEqual(self.plr.getBuys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Cathedral(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the start of your turn, trash a card from your hand."
        self.name = "Cathedral"
        self.cost = 3

    def hook_startTurn(self, game, player):
        player.plrTrashCard(num=1, force=True, prompt="Cathedral forces you to trash a card")


###############################################################################
class Test_Cathedral(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Cathedral'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_flag(self):
        self.plr.assign_project('Cathedral')
        self.g.print_state()
        self.plr.setHand('Copper', 'Estate', 'Province')
        self.plr.test_input = ['Copper']
        self.plr.startTurn()
        self.assertIsNotNone(self.g.inTrash('Copper'))
        self.assertIsNone(self.plr.inHand('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

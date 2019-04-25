#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Canal(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "During your turns, cards cost $1 less, but not less than $0."
        self.name = "Canal"
        self.cost = 7

    def hook_cardCost(self, game, player, card):
        """ All cards (including cards in players' hands) cost 1
            less this turn, but not less than 0 """
        return -1


###############################################################################
class Test_Canal(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Canal'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_cost(self):
        self.assertEqual(self.plr.cardCost(self.g['Gold']), 6)
        self.plr.assign_project('Canal')
        self.assertEqual(self.plr.cardCost(self.g['Gold']), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

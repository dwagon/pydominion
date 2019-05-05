#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Exploration(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "At the end of your Buy phase, if you didn't buy any cards, +1 Coffers and +1 Villager."
        self.name = "Exploration"
        self.cost = 4

    def hook_endBuyPhase(self, game, player):
        if player.stats['bought']:
            return
        player.gainCoffer(1)
        player.gainVillager(1)


###############################################################################
class Test_Exploration(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Exploration'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_play(self):
        self.plr.assign_project('Exploration')
        self.plr.test_input = ['End Phase']
        self.plr.buyPhase()
        self.assertEqual(self.plr.getCoffer(), 1)
        self.assertEqual(self.plr.getVillager(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

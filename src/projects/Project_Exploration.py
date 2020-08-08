#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Exploration(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = Card.PROJECT
        self.base = Game.RENAISSANCE
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
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Exploration'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        numc = self.plr.getCoffer()
        self.plr.assign_project('Exploration')
        self.plr.test_input = ['End Phase']
        self.plr.buy_phase()
        self.assertEqual(self.plr.getCoffer(), numc + 1)
        self.assertEqual(self.plr.getVillager(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

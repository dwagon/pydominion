#!/usr/bin/env python

import unittest
from dominion import Game, Project


###############################################################################
class Project_Guildhall(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "When you gain a Treasure, +1 Coffers."
        self.name = "Guildhall"
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if card.isTreasure():
            player.add_coffer()


###############################################################################
class Test_Guildhall(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=["Guildhall"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        numc = self.plr.getCoffer()
        self.plr.assign_project("Guildhall")
        self.plr.gainCard("Silver")
        self.assertEqual(self.plr.getCoffer(), numc + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

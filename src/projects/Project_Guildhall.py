#!/usr/bin/env python

import unittest
from Project import Project


###############################################################################
class Project_Guildhall(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = 'project'
        self.base = 'renaissance'
        self.desc = "When you gain a Treasure, +1 Coffers."
        self.name = "Guildhall"
        self.cost = 5

    def hook_gainCard(self, game, player, card):
        if card.isTreasure():
            player.gainCoffer()


###############################################################################
class Test_Guildhall(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Guildhall'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_play(self):
        self.plr.assign_project('Guildhall')
        self.plr.gainCard('Silver')
        self.assertEqual(self.plr.getCoffer(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

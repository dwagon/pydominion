#!/usr/bin/env python

import unittest
import Game
from Project import Project


###############################################################################
class Project_Academy(Project):
    def __init__(self):
        Project.__init__(self)
        self.cardtype = Card.PROJECT
        self.base = Game.RENAISSANCE
        self.desc = "When you gain an Action card, +1 Villager."
        self.name = "Academy"
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if card.isAction():
            player.output("Gained a villager from Academy")
            player.gainVillager()


###############################################################################
class Test_Academy(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initprojects=['Academy'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_have(self):
        self.assertEqual(self.plr.getVillager(), 0)
        self.plr.assign_project('Academy')
        self.plr.gainCard('Moat')
        self.assertEqual(self.plr.getVillager(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

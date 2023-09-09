#!/usr/bin/env python

import unittest
from dominion import Card, Game, Project


###############################################################################
class Project_Canal(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "During your turns, cards cost $1 less, but not less than $0."
        self.name = "Canal"
        self.cost = 7

    def hook_card_cost(self, game, player, card):
        """All cards (including cards in players' hands) cost 1
        less this turn, but not less than 0"""
        return -1


###############################################################################
class Test_Canal(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Canal"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_cost(self):
        self.assertEqual(self.plr.card_cost(self.g.get_card_from_pile("Gold")), 6)
        self.plr.assign_project("Canal")
        self.assertEqual(self.plr.card_cost(self.g.get_card_from_pile("Gold")), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

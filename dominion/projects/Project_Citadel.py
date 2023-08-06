#!/usr/bin/env python

import unittest
from dominion import Card, Game, Project


###############################################################################
class Project_Citadel(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "The first time you play an Action card during each of your turns, play it again afterward."
        self.name = "Citadel"
        self.cost = 8

    def hook_post_action(self, game, player, card):
        if player.played.size() == 1:
            player.output("Citadel plays {} again".format(card.name))
            player.play_card(card, discard=False, cost_action=False, post_action_hook=False)


###############################################################################
class Test_Citadel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initprojects=["Citadel"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.assign_project("Citadel")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_Citadel(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "The first time you play an Action card during each of your turns, play it again afterward."
        self.name = "Citadel"
        self.cost = 8

    def hook_post_play(self, game, player, card):
        if card.isAction() and player.piles[Piles.PLAYED].size() == 1:
            player.output(f"Citadel plays {card} again")
            player.play_card(
                card, discard=False, cost_action=False, post_action_hook=False
            )


###############################################################################
class TestCitadel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, projects=["Citadel"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.assign_project("Citadel")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

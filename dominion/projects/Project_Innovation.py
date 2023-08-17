#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Project


###############################################################################
class Project_Innovation(Project.Project):
    """Innovation"""

    def __init__(self):
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """The first time you gain an Action card in each of your turns,
            you may set it aside. If you do, play it."""
        self.name = "Innovation"
        self.cost = 6

    def hook_gain_card(self, game, player, card):
        """Gain a card"""
        if player.stats["gained"]:
            return {}
        if not card.isAction():
            return {}
        ch = player.plr_choose_options(
            f"Play {card.name} through Innovation?",
            ("Play card", True),
            ("Don't play", False),
        )
        if ch:
            player.add_card(card, Piles.HAND)
            player.play_card(card, cost_action=False)
        return {}


###############################################################################
class Test_Innovation(unittest.TestCase):
    """Test Innovation"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initprojects=["Innovation"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        """Play a card through innovation"""
        self.plr.assign_project("Innovation")
        self.plr.test_input = ["Play card"]
        self.plr.start_turn()
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])

    def test_dontplay(self):
        """Don't play a card through innovation"""
        self.plr.assign_project("Innovation")
        self.plr.test_input = ["Don't play"]
        self.plr.start_turn()
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])
        self.assertIsNotNone(self.plr.piles[Piles.DISCARD]["Moat"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

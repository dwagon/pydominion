#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Innovation"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Project, OptionKeys, Player


###############################################################################
class Project_Innovation(Project.Project):
    """Innovation"""

    def __init__(self) -> None:
        Project.Project.__init__(self)
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """Once during each of your turns, when you gain an Action card, you may play it."""
        self.name = "Innovation"
        self.cost = 6

    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        """Gain a card"""
        if not card.isAction():
            return {}
        if not player.do_once("Innovation"):
            player.output("Already used Innovation this turn")
            return {}
        if player.plr_choose_options(
            f"Play {card.name} through Innovation?",
            ("Play card", True),
            ("Don't play", False),
        ):
            player.add_card(card, Piles.HAND)
            player.play_card(card, cost_action=False)
        return {}


###############################################################################
class Test_Innovation(unittest.TestCase):
    """Test Innovation"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, projects=["Innovation"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Play a card through innovation"""
        self.plr.assign_project("Innovation")
        self.plr.test_input = ["Play card"]
        self.plr.start_turn()
        self.plr.gain_card("Moat")
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])

    def test_dontplay(self) -> None:
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

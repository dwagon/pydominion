#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Wolf_Den"""
import unittest
from collections import defaultdict
from typing import DefaultDict

from dominion import Card, Game, Piles, Landmark, Player


###############################################################################
class Landmark_Wolf_Den(Landmark.Landmark):
    """Wolf Den"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When scoring, -3VP per card you have exactly one copy of."""
        self.name = "Wolf Den"

    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        """Scoring"""
        score = 0
        cards: DefaultDict[str, int] = defaultdict(int)
        for card in player.all_cards():
            cards[card.name] += 1
        for card_name, num in cards.items():
            if num == 1:
                score -= 3
                player.output(f"Wolf Den: -3 due to only one {card_name}")
        player.add_score("Wolf Den", score)


###############################################################################
class Test_Wolf_Den(unittest.TestCase):
    """Test Wolf Den"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            landmarks=["Wolf Den"],
            badcards=[
                "Shepherd",
                "Pooka",
                "Fool",
                "Tracker",
                "Cemetery",
                "Pixie",
                "Secret Cave",
            ],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self) -> None:
        """Use Wolf Den"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver")
        self.plr.game_over()
        try:
            self.assertEqual(self.plr.get_score_details()["Wolf Den"], -6)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

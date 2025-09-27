#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Triumphal_Arch"""
import unittest
from collections import defaultdict
from typing import DefaultDict

from dominion import Card, Game, Piles, Landmark, Player


###############################################################################
class Landmark_Triumphal_Arch(Landmark.Landmark):
    """Triumphal Arch"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When scoring, 3VP per copy you have of the 2nd most common
        Action card among your cards (if it's a tie, count either)."""
        self.name = "Triumphal Arch"

    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        cards: DefaultDict[str, int] = defaultdict(int)
        for card in player.all_cards():
            if card.isAction():
                cards[card.name] += 1
        nums = sorted(cards.values())
        try:
            player.add_score("Triumphal Arch", nums[-2] * 3)
        except IndexError:
            player.output("No score from Triumphal Arch as insufficient action cards")


###############################################################################
class Test_Triumphal_Arch(unittest.TestCase):
    """Test Triumphal Arch"""

    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            landmarks=["Triumphal Arch"],
            initcards=["Moat", "Militia"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Test Triumphal Arch"""
        self.plr.piles[Piles.HAND].set("Moat", "Moat", "Moat")
        self.plr.piles[Piles.DECK].set("Militia", "Militia", "Militia", "Militia")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Triumphal Arch"], 3 * 3)

    def test_no_actions(self) -> None:
        """Test Triumphal Arch"""
        self.plr.piles[Piles.HAND].set("Copper", "Copper", "Copper")
        self.plr.piles[Piles.DECK].set("Duchy", "Duchy", "Duchy", "Duchy")
        self.plr.game_over()
        sd = self.plr.get_score_details()
        self.assertNotIn("Triumphal Arch", sd)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Wall"""
import unittest

from dominion import Card, Game, Piles, Landmark, Player


###############################################################################
class Landmark_Wall(Landmark.Landmark):
    """Wall"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When scoring, -1VP per card you have after the first 15."""
        self.name = "Wall"

    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        num_cards = len(player.all_cards())
        score = min(0, -(num_cards - 15))
        player.add_score("Wall", score)


###############################################################################
class Test_Wall(unittest.TestCase):
    """Test Wall"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Wall"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_lots_of_cards(self) -> None:
        """More than 15 cards"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Wall"], -3)

    def test_few_cards(self) -> None:
        """Less than 15 cards"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Copper")
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Copper")
        self.plr.piles[Piles.HAND].set("Gold", "Silver", "Copper")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Wall"], 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

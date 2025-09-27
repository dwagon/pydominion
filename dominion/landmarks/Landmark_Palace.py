#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Palace"""
import unittest

from dominion import Card, Game, Piles, Landmark, Player


###############################################################################
class Landmark_Palace(Landmark.Landmark):
    """Palace"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When scoring, 3VP per set you have of Copper - Silver - Gold."""
        self.name = "Palace"

    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        num = {"Copper": 0, "Silver": 0, "Gold": 0}
        for card in player.all_cards():
            if card.name in num:
                num[card.name] += 1
        score = min(num.values()) * 3
        player.output(f"Palace scored {score} VP ({num['Copper']} Copper, {num['Silver']} Silver, {num['Gold']} Gold)")
        player.add_score("Palace", score)


###############################################################################
class Test_Palace(unittest.TestCase):
    """Palace"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Palace"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Palace"""
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Silver", "Copper", "Duchy")
        self.plr.piles[Piles.DECK].set("Gold", "Silver", "Copper", "Copper", "Duchy")
        self.plr.piles[Piles.HAND].set("Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Palace"], 2 * 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

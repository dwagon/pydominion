#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Tower"""
import unittest
from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Tower(Landmark.Landmark):
    """Tower"""

    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = (
            "When scoring, 1VP per non-Victory card you have from an empty Supply pile."
        )
        self.name = "Tower"

    def hook_end_of_game(self, game, player):
        player.add_score("Tower", 0)
        for card in player.all_cards():
            if card.isVictory():
                continue
            if game.card_piles[card.pile].is_empty():
                player.add_score("Tower", 1)


###############################################################################
class TestTower(unittest.TestCase):
    """Test Tower"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Tower"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_none(self):
        """Use Tower"""
        self.plr.piles[Piles.HAND].set("Moat", "Moat")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Tower"], 0)

    def test_one(self):
        self.plr.piles[Piles.HAND].set("Moat", "Moat")
        while True:
            c = self.g.get_card_from_pile("Moat")
            if not c:
                break
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Tower"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

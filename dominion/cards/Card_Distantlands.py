#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_DistantLands(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.RESERVE,
            Card.CardType.VICTORY,
        ]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "Worth 4 VP if on your tavern mat at the end of the game, else 0"
        self.name = "Distant Lands"
        self.cost = 5
        self.callable = False
        self.counted = False

    def special_score(self, game, player) -> int:
        """Worth 4 VP if on your tavern mat; else 0"""
        if self.location == Piles.RESERVE:
            return 4
        return 0


###############################################################################
class TestDistantLands(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Distant Lands"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Distant Lands")

    def test_play(self):
        """Play a distant lands"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.RESERVE].size(), 1)
        self.assertIsNotNone(self.plr.piles[Piles.RESERVE]["Distant Lands"])

    def test_not_on_mat(self):
        self.plr.piles[Piles.HAND].set("Distant Lands")
        self.g.game_over = True
        self.assertEqual(self.plr.get_score_details()["Distant Lands"], 0)

    def test_on_mat(self):
        """Distant lands on mat"""
        self.plr.piles[Piles.RESERVE].set("Distant Lands")
        self.g.game_over = True
        self.assertEqual(self.plr.get_score_details()["Distant Lands"], 4)

    def test_on_mat_twice(self):
        """Two Distant lands on mat"""
        self.plr.piles[Piles.RESERVE].set("Distant Lands", "Distant Lands")
        self.g.game_over = True
        self.assertEqual(self.plr.get_score_details()["Distant Lands"], 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

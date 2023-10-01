#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Museum(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "When scoring, 2VP per differently named card you have."
        self.name = "Museum"

    def hook_end_of_game(self, game, player):
        c = set()
        for card in player.all_cards():
            c.add(card.name)
        player.add_score("Museum", len(c) * 2)


###############################################################################
class Test_Museum(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Museum"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Museum"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.piles[Piles.DISCARD].set("Gold", "Silver", "Copper")
        self.plr.piles[Piles.DECK].set("Gold", "Moat", "Moat")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Museum"], 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

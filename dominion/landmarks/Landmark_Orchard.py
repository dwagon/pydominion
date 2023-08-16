#!/usr/bin/env python

import unittest
from collections import defaultdict
from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Orchard(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "When scoring, 4VP per differently named Action card you have 3 or more copies of."
        self.name = "Orchard"

    def hook_end_of_game(self, game, player):
        actions = defaultdict(int)
        for card in player.all_cards():
            if card.isAction():
                actions[card.name] += 1
        score = sum([4 for x in actions.values() if x > 3])
        player.add_score("Orchard", score)


###############################################################################
class Test_Orchard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            landmarkcards=["Orchard"],
            initcards=["Moat", "Militia"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Orchard"""
        self.plr.piles[Piles.DISCARD].set("Moat", "Moat", "Militia", "Duchy")
        self.plr.piles[Piles.DECK].set("Moat", "Moat", "Copper", "Duchy")
        self.plr.piles[Piles.HAND].set("Moat", "Militia", "Copper", "Copper", "Duchy")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Orchard"], 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

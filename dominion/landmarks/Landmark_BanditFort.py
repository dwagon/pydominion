#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_BanditFort(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.desc = """When scoring, -2VP for each Silver and each Gold you have."""
        self.name = "Bandit Fort"

    def hook_end_of_game(self, game, player):
        score = 0
        for card in player.all_cards():
            if card.name in ("Silver", "Gold"):
                score -= 2
        player.add_score("Bandit Fort", score)


###############################################################################
class Test_BanditFort(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarkcards=["Bandit Fort"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Bandit Fort"""
        self.plr.piles[Piles.HAND].set("Gold", "Silver")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Bandit Fort"], -4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

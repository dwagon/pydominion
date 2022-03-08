#!/usr/bin/env python

import unittest
import Game
from Landmark import Landmark


###############################################################################
class Landmark_BanditFort(Landmark):
    def __init__(self):
        Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = """When scoring, -2VP for each Silver and each Gold you have."""
        self.name = "Bandit Fort"

    def hook_end_of_game(self, game, player):
        score = 0
        for card in player.allCards():
            if card.name in ("Silver", "Gold"):
                score -= 2
        player.addScore("Bandit Fort", score)


###############################################################################
class Test_BanditFort(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=["Bandit Fort"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Bandit Fort"""
        self.plr.setHand("Gold", "Silver")
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()["Bandit Fort"], -4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Museum(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "When scoring, 2VP per differently named card you have."
        self.name = "Museum"

    def hook_end_of_game(self, game, player):
        c = set()
        for card in player.allCards():
            c.add(card.name)
        player.addScore("Museum", len(c) * 2)


###############################################################################
class Test_Museum(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, landmarkcards=["Museum"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Museum"""
        self.plr.set_hand("Copper", "Estate")
        self.plr.set_discard("Gold", "Silver", "Copper")
        self.plr.set_deck("Gold", "Moat", "Moat")
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()["Museum"], 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

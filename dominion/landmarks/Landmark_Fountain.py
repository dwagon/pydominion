#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Fountain(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = "When scoring, 15VP if you have at least 10 Coppers."
        self.name = "Fountain"

    def hook_end_of_game(self, game, player):
        numcu = sum([1 for c in player.all_cards() if c.name == "Copper"])
        if numcu >= 10:
            player.add_score("Fountain", 15)
            player.output("Gained 15VP from Fountain")


###############################################################################
class Test_Fountain(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=["Fountain"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Fountain"""
        self.plr.set_discard("Copper", "Copper", "Copper", "Copper", "Copper", "Duchy")
        self.plr.set_deck("Copper", "Copper", "Copper", "Copper", "Copper", "Duchy")
        self.plr.gameOver()
        self.assertEqual(self.plr.getScoreDetails()["Fountain"], 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

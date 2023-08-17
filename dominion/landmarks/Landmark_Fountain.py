#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Fountain(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
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
        self.g = Game.TestGame(numplayers=1, landmarkcards=["Fountain"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Fountain"""
        self.plr.piles[Piles.DISCARD].set("Copper", "Copper", "Copper", "Copper", "Copper", "Duchy")
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Copper", "Copper", "Duchy")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Fountain"], 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

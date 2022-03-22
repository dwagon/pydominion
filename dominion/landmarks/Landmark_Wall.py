#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Wall(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.desc = """When scoring, -1VP per card you have after the first 15."""
        self.name = "Wall"

    def hook_end_of_game(self, game, player):
        ncards = len(player.all_cards())
        score = -(ncards - 15)
        player.add_score("Wall", score)


###############################################################################
class Test_Wall(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarkcards=["Wall"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Wall"""
        self.plr.set_discard("Gold", "Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.set_deck("Gold", "Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.set_hand("Gold", "Silver", "Copper", "Copper", "Copper", "Duchy")
        self.plr.game_over()
        self.assertEqual(self.plr.get_score_details()["Wall"], -3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

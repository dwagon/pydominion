#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Basilica(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Basilica"

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def desc(self, player):
        if self._vp <= 0:
            return "No effect"
        return (
            "When you buy a card, if you have 2 Coin or more left, take 2VP from here. (%d VP left)"
            % self._vp
        )

    def hook_buyCard(self, game, player, card):
        if self._vp <= 0:
            return
        if player.coin >= 2:
            player.output("Gained 2 VP from Basilica")
            self._vp -= 2
            player.add_score("Basilica", 2)


###############################################################################
class Test_Basilica(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, landmarkcards=["Basilica"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Basilica"""
        self.plr.coin = 4
        self.plr.buyCard(self.g["Copper"])
        self.assertEqual(self.plr.get_score_details()["Basilica"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

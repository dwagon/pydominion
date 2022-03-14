#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Colonnade(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Colonnade"

    def desc(self, player):
        if self._vp:
            return (
                "When you buy an Action card, if you have a copy of it in play, take 2VP from here. %d left"
                % self._vp
            )
        return "No VP left"

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_buy_card(self, game, player, card):
        if not card.isAction():
            return
        if not self._vp:
            return
        if player.in_played(card.name):
            self._vp -= 2
            player.add_score("Colonnade", 2)
            player.output("Gained 2VP from Colonnade")


###############################################################################
class Test_Colonnade(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, landmarkcards=["Colonnade"], initcards=["Moat"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Test Colonnade"""
        self.plr.set_played("Moat")
        self.plr.set_coins(5)
        self.plr.buy_card(self.g["Moat"])
        self.assertEqual(self.plr.get_score_details()["Colonnade"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

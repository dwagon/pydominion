#!/usr/bin/env python

import unittest
from dominion import Game, Landmark


###############################################################################
class Landmark_Aqueduct(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Game.EMPIRES
        self.name = "Aqueduct"
        self._goldvp = 8
        self._silvervp = 8
        self._vp = 0

    def desc(self, player):
        return """When you gain a Treasure, move 1 VP from its pile to this.
            When you gain a Victory card, take the VP from this.
            (Here: %d VP, Gold: %d VP, Silver: %d VP)""" % (
            self._vp,
            self._goldvp,
            self._silvervp,
        )

    def hook_gain_card(self, game, player, card):
        if card.name == "Gold":
            if self._goldvp:
                self._goldvp -= 1
                self._vp += 1
                player.output(
                    "%d VP left on Gold; %d VP on Aqueduct" % (self._goldvp, self._vp)
                )
        if card.name == "Silver":
            if self._silvervp:
                self._silvervp -= 1
                self._vp += 1
                player.output(
                    "%d VP left on Silver; %d VP on Aqueduct"
                    % (self._silvervp, self._vp)
                )
        if self._vp and card.isVictory():
            player.output("Gained %d VP from Aqueduct" % self._vp)
            player.add_score("Aqueduct", self._vp)
            self._vp = 0


###############################################################################
class Test_Aqueduct(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, landmarkcards=["Aqueduct"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain_silver(self):
        """Use Aqueduct gaining Silver"""
        self.plr.addBuys(2)
        self.plr.setCoin(20)
        self.plr.buy_card(self.g["Silver"])
        self.assertEqual(self.g.landmarks["Aqueduct"]._vp, 1)
        self.assertEqual(self.g.landmarks["Aqueduct"]._silvervp, 7)
        self.plr.buy_card(self.g["Duchy"])
        self.assertEqual(self.plr.get_score_details()["Aqueduct"], 1)

    def test_gain_gold(self):
        """Use Aqueduct gaining Gold"""
        self.plr.addBuys(2)
        self.plr.setCoin(20)
        self.plr.buy_card(self.g["Gold"])
        self.assertEqual(self.g.landmarks["Aqueduct"]._vp, 1)
        self.assertEqual(self.g.landmarks["Aqueduct"]._goldvp, 7)
        self.assertEqual(self.g.landmarks["Aqueduct"]._silvervp, 8)
        self.plr.buy_card(self.g["Duchy"])
        self.assertEqual(self.plr.get_score_details()["Aqueduct"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

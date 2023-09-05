#!/usr/bin/env python

import unittest
from dominion import Card, Game, Landmark


###############################################################################
class Landmark_Battlefield(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Battlefield"
        self._vp = 0

    def desc(self, player):
        return "When you gain a Victory card, take 2VP from here. (%d left)" % self._vp

    def hook_gain_card(self, game, player, card):
        if card.isVictory() and self._vp >= 0:
            self._vp -= 2
            player.output("Gained 2VP from Battlefield")
            player.add_score("Battlefield", 2)

    def setup(self, game):
        self._vp = 6 * game.numplayers


###############################################################################
class TestBattlefield(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            landmarkcards=["Battlefield"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self):
        """Use Battlefield"""
        self.plr.coins.set(5)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.get_score_details()["Battlefield"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

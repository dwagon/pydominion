#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Colonnade"""
import unittest

from dominion import Card, Game, Piles, Landmark


###############################################################################
class Landmark_Colonnade(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Colonnade"

    def dynamic_description(self, player):
        if self._vp:
            return (
                "When you buy an Action card, if you have a copy of it in play, take 2VP from here. %d left" % self._vp
            )
        return "No VP left"

    def setup(self, game):
        self._vp = 6 * game.numplayers

    def hook_buy_card(self, game, player, card):
        if not card.isAction():
            return
        if not self._vp:
            return
        if card.name in player.piles[Piles.PLAYED]:
            self._vp -= 2
            player.add_score("Colonnade", 2)
            player.output("Gained 2VP from Colonnade")


###############################################################################
class TestColonnade(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, landmarks=["Colonnade"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self):
        """Test Colonnade"""
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.coins.set(5)
        self.plr.buy_card("Moat")
        self.assertEqual(self.plr.get_score_details()["Colonnade"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

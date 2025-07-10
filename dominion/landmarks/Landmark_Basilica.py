#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Basilica"""
import unittest

from dominion import Card, Game, Landmark, Player


###############################################################################
class Landmark_Basilica(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Basilica"
        self._vp = 0

    def setup(self, game: Game.Game) -> None:
        self._vp = 6 * game.numplayers

    def dynamic_description(self, player: Player.Player) -> str:
        if self._vp <= 0:
            return "No effect"
        return f"When you buy a card, if you have 2 Coin or more left, take 2VP from here. ({self._vp} VP left)"

    def hook_buy_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> None:
        if self._vp <= 0:
            return
        if player.coins.get() >= 2:
            player.output("Gained 2 VP from Basilica")
            self._vp -= 2
            player.add_score("Basilica", 2)


###############################################################################
class TestBasilica(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Basilica"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self) -> None:
        """Use Basilica"""
        self.plr.coins.set(4)
        self.plr.buy_card("Copper")
        self.assertEqual(self.plr.get_score_details()["Basilica"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

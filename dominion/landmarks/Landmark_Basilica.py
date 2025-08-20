#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Basilica"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, Player, OptionKeys, Phase


###############################################################################
class Landmark_Basilica(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Basilica"
        self.vp = 0

    def setup(self, game: Game.Game) -> None:
        self.vp = 6 * game.numplayers

    def dynamic_description(self, player: Player.Player) -> str:
        if self.vp <= 0:
            return "No effect"
        return (
            f"When you gain a card in your Buy phase, if you have $2 or more, take 2VP from here. ({self.vp} VP left)"
        )

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if self.vp <= 0 or player.phase != Phase.BUY:
            return {}
        if player.coins.get() >= 2:
            player.output("Gained 2 VP from Basilica")
            self.vp -= 2
            player.add_score("Basilica", 2)
        return {}


###############################################################################
class TestBasilica(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Basilica"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain(self) -> None:
        """Use Basilica"""
        self.plr.coins.set(4)
        self.plr.phase = Phase.BUY
        self.plr.buy_card("Copper")
        self.assertEqual(self.plr.get_score_details()["Basilica"], 2)

    def test_gain_cheap(self) -> None:
        """Use Basilica with not enough money"""
        self.plr.coins.set(1)
        self.plr.buy_card("Copper")
        self.assertEqual(self.plr.get_score_details().get("Basilica", 0), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Colonnade"""
import unittest
from typing import Any

from dominion import Card, Game, Piles, Landmark, OptionKeys, Player, Phase


###############################################################################
class Landmark_Colonnade(Landmark.Landmark):
    def __init__(self):
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Colonnade"
        self.vp = 0

    def dynamic_description(self, player: "Player.Player") -> str:
        if self.vp:
            return f"""When you gain an Action card in your Buy phase, if you have a copy of it in play,
                take 2VP from here. {self.vp} left."""
        return "No VP left"

    def setup(self, game: "Game.Game") -> None:
        self.vp = 6 * game.numplayers

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if not card.isAction() or player.phase != Phase.BUY:
            return {}
        if not self.vp:
            return {}
        if card.name in player.piles[Piles.PLAYED]:
            self.vp -= 2
            player.add_score("Colonnade", 2)
            player.output("Gained 2VP from Colonnade")
        return {}


###############################################################################
class TestColonnade(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, landmarks=["Colonnade"], initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play(self) -> None:
        """Test Colonnade"""
        self.plr.phase = Phase.BUY
        self.plr.piles[Piles.PLAYED].set("Moat")
        self.plr.coins.set(5)
        self.plr.buy_card("Moat")
        self.assertEqual(self.plr.get_score_details()["Colonnade"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

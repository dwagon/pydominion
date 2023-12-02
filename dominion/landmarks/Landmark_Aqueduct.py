#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Aqueduct"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, OptionKeys, Player


###############################################################################
class Landmark_Aqueduct(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Aqueduct"
        self._goldvp = 8
        self._silvervp = 8
        self._vp = 0

    def dynamic_description(self, player: Player.Player) -> str:
        return f"""When you gain a Treasure, move 1 VP from its pile to this.
            When you gain a Victory card, take the VP from this.
            (Here: {self._vp} VP, Gold: {self._goldvp} VP, Silver: {self._silvervp} VP)"""

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if card.name == "Gold":
            if self._goldvp:
                self._goldvp -= 1
                self._vp += 1
                player.output(
                    f"{self._goldvp} VP left on Gold; {self._vp }VP on Aqueduct"
                )
        if card.name == "Silver":
            if self._silvervp:
                self._silvervp -= 1
                self._vp += 1
                player.output(
                    f"{self._silvervp} VP left on Silver; {self._vp} VP on Aqueduct"
                )
        if self._vp and card.isVictory():
            player.output(f"Gained {self._vp} VP from Aqueduct")
            player.add_score("Aqueduct", self._vp)
            self._vp = 0
        return {}


###############################################################################
class TestAqueduct(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, landmarks=["Aqueduct"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain_silver(self) -> None:
        """Use Aqueduct gaining Silver"""
        self.plr.buys.add(2)
        self.plr.coins.set(20)
        self.plr.buy_card("Silver")
        self.assertEqual(self.g.landmarks["Aqueduct"]._vp, 1)
        self.assertEqual(self.g.landmarks["Aqueduct"]._silvervp, 7)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.get_score_details()["Aqueduct"], 1)

    def test_gain_gold(self) -> None:
        """Use Aqueduct gaining Gold"""
        self.plr.buys.add(2)
        self.plr.coins.set(20)
        self.plr.buy_card("Gold")
        self.assertEqual(self.g.landmarks["Aqueduct"]._vp, 1)
        self.assertEqual(self.g.landmarks["Aqueduct"]._goldvp, 7)
        self.assertEqual(self.g.landmarks["Aqueduct"]._silvervp, 8)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.get_score_details()["Aqueduct"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

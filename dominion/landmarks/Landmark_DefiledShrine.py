#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Defiled_Shrine"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, Player, OptionKeys, Phase


###############################################################################
class Landmark_DefiledShrine(Landmark.Landmark):
    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Defiled Shrine"
        self.required_cards = ["Curse"]
        self.stored_vp = 0
        self.desc = f"""When you gain an Action, move 1 VP from its pile to this.
                When you gain a Curse in your Buy phase, take the VP from this."""

    @classmethod
    def setup(cls, game: "Game.Game") -> None:
        cls.vp: dict[str, int] = {}  # type: ignore
        for name, _ in game.get_card_piles():
            card = game.card_instances[name]
            if card and not card.isGathering() and card.isAction():
                cls.vp[name] = 2  # type: ignore

    def hook_all_players_gain_card(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card.Card",
    ) -> dict[OptionKeys, Any]:
        if player != owner:
            return {}
        if card.name not in game.landmarks["Defiled Shrine"].vp:
            return {}
        if game.landmarks["Defiled Shrine"].vp[card.name]:  # type: ignore
            game.landmarks["Defiled Shrine"].vp[card.name] -= 1  # type: ignore
            self.stored_vp += 1

        return {}

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        if card.name == "Curse" and player.phase == Phase.BUY:
            player.add_score("Defiled Shrine", self.stored_vp)
            self.stored_vp = 0
        return {}


###############################################################################
class TestDefiledShrine(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=2,
            landmarks=["Defiled Shrine"],
            initcards=["Moat"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_use(self) -> None:
        """Use Defiled Shrine"""
        self.plr.buys.set(2)
        self.plr.phase = Phase.BUY
        self.plr.coins.set(5)
        self.assertEqual(self.g.landmarks["Defiled Shrine"].vp["Moat"], 2)  # type: ignore
        self.plr.buy_card("Moat")
        self.assertEqual(self.g.landmarks["Defiled Shrine"].vp["Moat"], 1)  # type: ignore
        self.plr.buy_card("Curse")
        self.assertEqual(self.plr.score["Defiled Shrine"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

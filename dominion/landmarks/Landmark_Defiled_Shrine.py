#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Defiled_Shrine"""
import unittest
from typing import Any

from dominion import Card, Game, Landmark, Player, OptionKeys, Phase

DEFILED = "defiled shrine"


###############################################################################
class Landmark_Defiled_Shrine(Landmark.Landmark):
    """Defiled Shrine"""

    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.EMPIRES
        self.name = "Defiled Shrine"
        self.required_cards = ["Curse"]
        self.stored_vp = 0

    def dynamic_description(self, player: "Player.Player") -> str:
        return f"""When you gain an Action, move 1 VP from its pile to this.
                When you gain a Curse in your Buy phase, take the {self.stored_vp} VP from this."""

    def setup(self, game: "Game.Game") -> None:
        """Setup: Put 2VP on each non-Gathering Action Supply pile."""
        game.specials[DEFILED] = {}
        for name, _ in game.get_card_piles():
            card = game.card_instances[name]
            if card and not card.isGathering() and card.isAction():
                game.specials[DEFILED][name] = 2

    def hook_all_players_gain_card(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card.Card",
    ) -> dict[OptionKeys, Any]:
        """When you gain an Action, move 1VP from its pile to this."""
        if player != owner:
            return {}
        if card.name not in game.specials[DEFILED]:
            return {}
        if game.specials[DEFILED][card.name]:
            game.specials[DEFILED][card.name] -= 1
            self.stored_vp += 1

        return {}

    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card.Card") -> dict[OptionKeys, Any]:
        """When you gain a Curse in your Buy phase, take the VP from this."""
        if card.name == "Curse" and player.phase == Phase.BUY:
            player.add_score("Defiled Shrine", self.stored_vp)
            self.stored_vp = 0
        return {}


###############################################################################
class TestDefiled_Shrine(unittest.TestCase):
    """Test Defiled Shrine"""

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
        self.assertEqual(self.g.specials[DEFILED]["Moat"], 2)
        self.plr.buy_card("Moat")
        self.assertEqual(self.g.specials[DEFILED]["Moat"], 1)
        self.plr.buy_card("Curse")
        self.assertEqual(self.plr.score["Defiled Shrine"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

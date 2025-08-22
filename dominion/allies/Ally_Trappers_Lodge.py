#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Trappers%27_Lodge"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Ally, Player, OptionKeys


###############################################################################
class Ally_Trappers_Lodge(Ally.Ally):
    def __init__(self) -> None:
        Ally.Ally.__init__(self)
        self.base = Card.CardExpansion.ALLIES
        self.desc = (
            """When you gain a card, you may spend a Favor to put it onto your deck."""
        )
        self.name = "Trappers' Lodge"

    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if not player.favors.get():
            return {}
        if player.plr_choose_options(
            "Use Trappers Lodge to put it onto your deck for a favour?",
            ("Do nothing", False),
            ("Put on to deck", True),
        ):
            player.favors.add(-1)
            return {OptionKeys.DESTINATION: Piles.TOPDECK}
        return {}


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):
    return []


###############################################################################
class TestTrappersLodge(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1, allies="Trappers Lodge", initcards=["Underling"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_gain_card(self) -> None:
        """Add to top deck"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper")
        self.plr.favors.set(2)
        self.plr.test_input = ["Put on to deck"]
        self.plr.gain_card("Estate")
        self.assertEqual(self.plr.piles[Piles.DECK].top_card().name, "Estate")
        self.assertEqual(self.plr.favors.get(), 1)

    def test_keep(self) -> None:
        """Do nothing"""
        self.plr.piles[Piles.DECK].set("Copper", "Copper")
        self.plr.favors.set(2)
        self.plr.test_input = ["Do nothing"]
        self.plr.gain_card("Estate")
        self.assertNotEqual(self.plr.piles[Piles.DECK].top_card().name, "Estate")
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.favors.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

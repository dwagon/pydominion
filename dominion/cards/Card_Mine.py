#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Mine"""

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Mine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = (
            "You may trash a Treasure from your hand. Gain a Treasure to your hand costing up to $3 more than it."
        )
        self.name = "Mine"
        self.cost = 5

    def _generate_options(self, player: "Player.Player") -> list[dict[str, Any]]:
        """Generate the options for player dialog"""
        options: list[dict[str, Any]] = [{"selector": "0", "print": "Don't trash a card", "card": None}]
        index = 1
        for card in player.piles[Piles.HAND]:
            if card.isTreasure():
                options.append(
                    {
                        "selector": f"{index}",
                        "print": f"Trash/Upgrade {card.name}",
                        "card": card,
                    }
                )
                index += 1
        return options

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Trash a treasure card from your hand. Gain a treasure card
        costing up to 3 more, put it in your hand"""
        options = self._generate_options(player)
        player.output("Trash a treasure to gain a better one")
        o = player.user_input(options, "Trash which treasure?")
        if o["card"]:
            val = o["card"].cost
            if gained_card := player.plr_gain_card(
                cost=val + 3, modifier="equal", destination=Piles.HAND, types={Card.CardType.TREASURE: True}
            ):
                player.output(f"Converted to {gained_card.name}")
                player.trash_card(o["card"])


###############################################################################
class TestMine(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Mine"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Mine")

    def test_convert_copper(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Upgrade Copper", "Get Silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.HAND])
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.actions.get(), 0)

    def test_convert_nothing(self) -> None:
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND][0].name, "Copper")
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

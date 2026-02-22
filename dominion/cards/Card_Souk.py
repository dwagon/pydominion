#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Souk"""

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, OptionKeys


###############################################################################
class Card_Souk(Card.Card):
    """Souk"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+1 Buy; +$7; –$1 per card in your hand (you can't go below $0).
        When you gain this, trash up to 2 cards from your hand."""
        self.buys = 1
        self.name = "Souk"
        self.cost = 5

    def special(self, game: Game.Game, player: Player.Player) -> None:
        """+$7; –$1 per card in your hand (you can't go below $0)"""
        player.coins.add(7)
        player.coins.add(-len(player.piles[Piles.HAND]))
        if player.coins.get() < 0:
            player.coins.set(0)

    def hook_gain_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        """When you gain this, trash up to 2 cards from your hand."""
        player.plr_trash_card(num=2)
        return {}


###############################################################################
class TestSouk(unittest.TestCase):
    """Test Souk"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Souk", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Souk")

    def test_play(self) -> None:
        """Play a card"""
        self.plr.piles[Piles.HAND].set("Copper", "Duchy", "Estate")
        buys = self.plr.buys.get()
        coins = self.plr.coins.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys + 1)
        self.assertEqual(self.plr.coins.get(), coins + 4)

    def test_play_negative(self) -> None:
        """Play a card but lose money - ensure we don't go below zero"""
        self.plr.piles[Piles.HAND].set(
            "Copper",
            "Copper",
            "Silver",
            "Silver",
            "Gold",
            "Gold",
            "Duchy",
            "Estate",
            "Province",
        )
        self.plr.coins.set(1)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_gain_card(self) -> None:
        """Gain the card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.test_input = ["Trash Copper", "Trash Silver", "Finish"]
        self.plr.gain_card("Souk")
        self.assertIn("Silver", self.g.trash_pile)
        self.assertIn("Copper", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

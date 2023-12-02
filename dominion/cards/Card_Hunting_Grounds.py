#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Game, Card, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_HuntingGrounds(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+4 Cards; When you trash this, gain a Duchy or 3 Estates."""
        self.name = "Hunting Grounds"
        self.cards = 4
        self.cost = 6

    def hook_trash_this_card(
        self, game: Game.Game, player: Player.Player
    ) -> dict[OptionKeys, Any]:
        choice = player.plr_choose_options(
            "What to gain?", ("Gain a duchy", "duchy"), ("Gain 3 Estates", "estates")
        )
        if choice == "duchy":
            player.gain_card("Duchy")
        if choice == "estates":
            for _ in range(3):
                try:
                    player.gain_card("Estate")
                except NoCardException:
                    player.output("No more Estates")
                    break
        return {}


###############################################################################
class TestHuntingGrounds(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Hunting Grounds"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Hunting Grounds")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a Hunting Ground"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 4)

    def test_trash_estate(self) -> None:
        """Trash a hunting ground and gain estates"""
        self.plr.test_input = ["Estates"]
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)
        self.assertIn("Estate", self.plr.piles[Piles.DISCARD])

    def test_trash_duchy(self) -> None:
        """Trash a hunting ground and gain duchy"""
        self.plr.test_input = ["Duchy"]
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

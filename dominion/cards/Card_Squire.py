#!/usr/bin/env python

import unittest
from typing import Optional, Any

from dominion import Game, Card, Piles, Player, NoCardException, OptionKeys


###############################################################################
class Card_Squire(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Coin. Choose one: +2 Actions; or +2 Buys; or gain a Silver.
        When you trash this, gain an Attack card."""
        self.name = "Squire"
        self.cost = 2
        self.coin = 1

    def special(self, game: Game.Game, player: Player.Player) -> None:
        choice = player.plr_choose_options(
            "Choose one.",
            ("+2 Actions", "actions"),
            ("+2 Buys", "buys"),
            ("Gain a Silver", "silver"),
        )
        if choice == "actions":
            player.add_actions(2)
        elif choice == "buys":
            player.buys.add(2)
        elif choice == "silver":
            try:
                player.gain_card("Silver")
            except NoCardException:
                player.output("No more Silver")

    def hook_trash_this_card(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        attacks = []
        for name, _ in game.get_card_piles():
            card = game.card_instances[name]
            if card.isAttack() and card.purchasable:
                attacks.append(card)
        cards = player.card_sel(prompt="Gain an attack card", cardsrc=attacks)
        if not cards:
            player.output("No suitable cards")
            return {}
        try:
            player.gain_card(cards[0].name)
            player.output(f"No more {cards[0].name}")
        except NoCardException:
            return {}
        return {}


###############################################################################
class TestSquire(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Squire", "Militia"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Squire")

    def test_play_actions(self) -> None:
        """Play a Squire - gain actions"""
        self.plr.test_input = ["action"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_buys(self) -> None:
        """Play a Squire - gain buys"""
        self.plr.test_input = ["buys"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.buys.get(), 3)
        self.assertNotIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_play_silver(self) -> None:
        """Play a Squire - gain Silver"""
        self.plr.test_input = ["silver"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])

    def test_trash(self) -> None:
        """Trash a Squire"""
        self.plr.test_input = ["militia"]
        self.plr.trash_card(self.card)
        self.assertIn("Militia", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

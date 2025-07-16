#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, PlayArea, Game, Piles, Player, OptionKeys


###############################################################################
class Card_CargoShip(Card.Card):
    """Cargo Ship"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.RENAISSANCE
        self.name = "Cargo Ship"
        self.desc = """+2 Coin; Once this turn, when you gain a card, you may
            set it aside face up (on this). At the start of your next turn,
            put it into your hand."""
        self.cost = 3
        self.coin = 2
        self._cargo_ship = PlayArea.PlayArea("Cargo Ship", initial=[])

    ###########################################################################
    def hook_gain_card(self, game: Game.Game, player: Player.Player, card: Card.Card) -> dict[OptionKeys, Any]:
        if self not in player.piles[Piles.DURATION]:
            return {}
        if card.location != Piles.CARDPILE:
            return {}
        if not self._cargo_ship:
            if player.plr_choose_options(
                f"Do you want to set {card.name} aside to play next turn?",
                ("Yes", True),
                ("No", False),
            ):
                player.secret_count += 1
                player.move_card(card, self._cargo_ship)
                return {OptionKeys.DONTADD: True}
        return {}

    ###########################################################################
    def duration(self, game: Game.Game, player: Player.Player) -> dict[OptionKeys, Any]:
        for card in self._cargo_ship:
            player.add_card(card, Piles.HAND)
            self._cargo_ship.remove(card)
            player.secret_count -= 1
        return {}


###############################################################################
class TestCargoShip(unittest.TestCase):
    """Test Cargo Ship"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Cargo Ship", "Moat"], badcards=["Shaman"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_play_card_yes(self) -> None:
        self.card = self.g.get_card_from_pile("Cargo Ship")
        self.card.hook_gain_this_card(self.g, self.plr)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.test_input = ["Yes"]
        self.plr.buy_card("Moat")
        self.assertEqual(self.card._cargo_ship[0].name, "Moat")
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.HAND])

    def test_play_card_no(self) -> None:
        self.card = self.g.get_card_from_pile("Cargo Ship")
        self.card.hook_gain_this_card(self.g, self.plr)
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.plr.test_input = ["No"]
        self.plr.buy_card("Moat")
        self.assertEqual(len(self.card._cargo_ship), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertNotIn("Moat", self.plr.piles[Piles.HAND])

    def test_play_cargo_twice(self) -> None:
        """If we have two cargo ships active at the same time we shouldn't be able to set aside a card twice"""
        self.plr.add_actions(2)
        self.plr.test_input = ["Yes", "Yes"]
        self.card1 = self.g.get_card_from_pile("Cargo Ship")
        self.plr.add_card(self.card1, Piles.HAND)
        self.plr.play_card(self.card1)
        self.card2 = self.g.get_card_from_pile("Cargo Ship")
        self.plr.add_card(self.card2, Piles.HAND)
        self.assertEqual(len(self.card1._cargo_ship) + len(self.card2._cargo_ship), 0)
        self.plr.play_card(self.card2)
        self.plr.buy_card("Moat")
        # Only one cargo ship should have the moat
        self.assertEqual(len(self.card1._cargo_ship) + len(self.card2._cargo_ship), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

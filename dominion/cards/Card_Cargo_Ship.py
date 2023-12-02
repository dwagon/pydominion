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
        self._cargo_ship = PlayArea.PlayArea([])

    ###########################################################################
    def hook_gain_card(
        self, game: Game.Game, player: Player.Player, card: Card.Card
    ) -> dict[OptionKeys, Any]:
        if self not in player.piles[Piles.DURATION]:
            return {}
        if not self._cargo_ship:
            if player.plr_choose_options(
                f"Do you want to set {card.name} aside to play next turn?",
                ("Yes", True),
                ("No", False),
            ):
                self._cargo_ship.add(card)
                player.secret_count += 1
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
        self.g = Game.TestGame(
            numplayers=1, initcards=["Cargo Ship", "Moat"], badcards=["Shaman"]
        )
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


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

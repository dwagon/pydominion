#!/usr/bin/env python

import unittest
from typing import Any

from dominion import Card, Game, Piles, Player, NoCardException


###############################################################################
class Card_Duchess(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+2 Coin.  Each player (including you) looks at the top card of his deck,
            and discards it or puts it back."""
        self.name = "Duchess"
        self.coin = 2
        self.cost = 2

    def special(self, game: Game.Game, player: Player.Player) -> None:
        for plr in game.player_list():
            try:
                card = plr.next_card()
            except NoCardException:
                continue
            name = "your" if plr == player else f"{player}'s"
            if plr.plr_choose_options(
                f"Due to {name} Duchess you can keep or discard the top card",
                (f"Keep {card} on top of deck", True),
                (f"Discard {card}", False),
            ):
                plr.add_card(card, "topdeck")
            else:
                plr.output(f"Discarding {card}")
                plr.discard_card(card)


###############################################################################
def botresponse(
    player: Player.Player, kind: str, args: Any = None, kwargs: Any = None
) -> Any:  # pragma: no cover
    if "Estate" in args[0] or "Duchy" in args[0] or "Province" in args[0]:
        return False
    return True


###############################################################################
class TestDuchess(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Duchess")

    def test_play(self) -> None:
        """Play duchess - keep on deck"""
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["keep"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Province", self.plr.piles[Piles.DECK])
        self.assertNotIn("Province", self.plr.piles[Piles.DISCARD])

    def test_disacrd(self) -> None:
        """Play duchess - discard"""
        self.plr.piles[Piles.DECK].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertNotIn("Province", self.plr.piles[Piles.DECK])
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])

    def test_buy_duchess(self) -> None:
        self.plr.test_input = ["Duchess"]
        self.plr.gain_card("Duchy")
        self.assertIn("Duchess", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])

    def test_buy_duchy(self) -> None:
        self.plr.test_input = ["No"]
        self.plr.gain_card("Duchy")
        self.assertNotIn("Duchess", self.plr.piles[Piles.DISCARD])
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

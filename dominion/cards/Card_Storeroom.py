#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Storeroom"""
import unittest
from dominion import Game, Card, Piles, Player


###############################################################################
class Card_Storeroom(Card.Card):
    """Storeroom"""

    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Buy; Discard any number of cards. +1 Card per card
            discarded. Discard any number of cards. +1 Coin per card discarded
            the second time """
        self.name = "Store Room"
        self.buys = 1
        self.cost = 3

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Discard any number of cards. +1 Card per card discarded.
        Discard any number of cards. +1 Coin per card discarded the
        second time"""
        if to_discard := player.plr_discard_cards(
            0,
            any_number=True,
            prompt="Discard any number of cards. +1 Card per card discarded",
        ):
            player.output(f"Gaining {len(to_discard)} cards from Storeroom")
            player.pickup_cards(len(to_discard))
        player.output("Discard any number of cards. +1 Coin per card discarded")
        if to_discard := player.plr_discard_cards(0, any_number=True):
            player.output(f"Gaining {len(to_discard)} coins from Storeroom")
            player.coins.add(len(to_discard))


###############################################################################
class TestStoreroom(unittest.TestCase):
    """Test Storeroom"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Store Room"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Store Room")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self) -> None:
        """Play a store room"""
        self.plr.test_input = ["0", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())

    def test_discard_once(self) -> None:
        """Storeroom: Only discard during the first discard phase"""
        self.plr.test_input = ["1", "0", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 - 1 + 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_discard_twice(self) -> None:
        """Storeroom: Discard during the both discard phases"""
        self.plr.test_input = ["1", "0", "1", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 - 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

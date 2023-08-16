#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Storeroom(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Buy; Discard any number of cards. +1 Card per card
            discarded. Discard any number of cards. +1 Coin per card discarded
            the second time """
        self.name = "Store Room"
        self.buys = 1
        self.cost = 3

    def special(self, game, player):
        """Discard any number of cards. +1 Card per card discarded.
        Discard any number of cards. +1 Coin per card discarded the
        second time"""
        todiscard = player.plr_discard_cards(
            0,
            any_number=True,
            prompt="Discard any number of cards. +1 Card per card discarded",
        )
        player.output("Gaining %d cards from Storeroom" % len(todiscard))
        player.pickup_cards(len(todiscard))
        player.output("Discard any number of cards. +1 Coin per card discarded")
        todiscard = player.plr_discard_cards(0, any_number=True)
        player.output("Gaining %d coins from Storeroom" % len(todiscard))
        player.coins.add(len(todiscard))


###############################################################################
class Test_Storeroom(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Store Room"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Store Room"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a store room"""
        self.plr.test_input = ["0", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())

    def test_discardonce(self):
        """Storeroom: Only discard during the first discard phase"""
        self.plr.test_input = ["1", "0", "0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 - 1 + 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_discardtwice(self):
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

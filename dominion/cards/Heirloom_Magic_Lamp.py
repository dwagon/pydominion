#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_MagicLamp(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.HEIRLOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """+1 Coin; When you play this, if there are at least 6 cards
            that you have exactly 1 copy of in play, trash this. If you do,
            gain 3 Wishes from their pile."""
        self.name = "Magic Lamp"
        self.cost = 0
        self.coin = 1
        self.purchasable = False
        self.required_cards = [("Card", "Wish")]

    def special(self, game, player):
        cards = []
        for c in player.piles[Piles.PLAYED]:
            if player.piles[Piles.PLAYED].count(c) == 1:
                cards.append(c)
        if len(cards) >= 6:
            player.trash_card(self)
            for _ in range(3):
                player.gain_card("Wish")


###############################################################################
class Test_MagicLamp(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Secret Cave"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Magic Lamp")

    def test_play_gain(self):
        """Play a Magic Lamp to gain 3 Wishes"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Gold", "Duchy", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertIn("Wish", self.plr.piles[Piles.DISCARD])

    def test_play_fail(self):
        """Play a Magic Lamp but don't gain wishes"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Gold", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertNotIn("Wish", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

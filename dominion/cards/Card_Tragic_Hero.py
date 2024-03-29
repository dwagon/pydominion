#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Tragic_Hero(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = (
            "+3 Cards; +1 Buys; If you have 8 or more cards in hand (after drawing), trash this and gain a Treasure."
        )
        self.name = "Tragic Hero"
        self.cost = 5
        self.cards = 3
        self.buys = 1

    def special(self, game, player):
        if player.piles[Piles.HAND].size() >= 8:
            player.trash_card(self)
            player.plr_gain_card(cost=None, types={Card.CardType.TREASURE: True})


###############################################################################
class Test_Tragic_Hero(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Tragic Hero"], badcards=["Fool's Gold"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Tragic Hero")

    def test_play(self):
        """Play a Tragic Hero with less than 8 cards"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1 + 3)

    def test_gainsomething(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Get Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 3)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

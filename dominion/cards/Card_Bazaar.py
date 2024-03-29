#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Bazaar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.desc = "+1 cards, +2 action, +1 coin"
        self.name = "Bazaar"
        self.base = Card.CardExpansion.SEASIDE
        self.cards = 1
        self.actions = 2
        self.coin = 1
        self.cost = 5


###############################################################################
class Test_Bazaar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bazaar"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Bazaar")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play Bazaar"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

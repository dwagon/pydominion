#!/usr/bin/env python

import unittest
from dominion import Game, Piles, Card
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_DameJosephine(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.KNIGHT,
            Card.CardType.VICTORY,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Dame Josephine"
        self.desc = """+2 VP. Each other player reveals the top 2 cards of his deck,
            trashes one of them costing from 3 to 6, and discards the rest.
            If a Knight is trashed by this, trash this card."""
        self.cost = 5
        self.victory = 2

    def special(self, game, player):
        """Each other player reveals the top 2 cards of his deck,
        trashes one of them costing from 3 to 6 and discards the
        rest. If a knight is trashed by this, trash this card"""
        self.knight_special(game, player)


###############################################################################
class TestDameJosephine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Knights"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        while True:
            self.card = self.g.get_card_from_pile("Knights")
            if self.card.name == "Dame Josephine":
                break

    def test_score(self):
        """Play the Dame"""
        self.plr.add_card(self.card, Piles.HAND)
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Dame Josephine"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

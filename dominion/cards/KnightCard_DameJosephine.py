#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Card
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_Dame_Josephine(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [
            Card.TYPE_ACTION,
            Card.TYPE_ATTACK,
            Card.TYPE_KNIGHT,
            Card.TYPE_VICTORY,
        ]
        self.base = Game.DARKAGES
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
class Test_Dame_Josephine(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Knight"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Knight"].remove()
            if self.card.name == "Dame Josephine":
                break

    def test_score(self):
        """Play the Dame"""
        self.plr.addCard(self.card, "hand")
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc["Dame Josephine"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

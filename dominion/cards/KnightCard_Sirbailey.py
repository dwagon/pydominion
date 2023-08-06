#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Card
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_Sir_Bailey(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.KNIGHT,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Sir Bailey"
        self.desc = """+1 Card +1 Action.
            Each other player reveals the top 2 cards of his deck, trashes one of them
            costing from 3 to 6, and discards the rest.
            If a Knight is trashed by this, trash this card."""
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        self.knight_special(game, player)


###############################################################################
class Test_Sir_Bailey(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Knights"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Knights"].remove()
            if self.card.name == "Sir Bailey":
                break

    def test_score(self):
        """Play the Sir"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

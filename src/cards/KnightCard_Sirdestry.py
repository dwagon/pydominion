#!/usr/bin/env python

import unittest
import Game
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Sir_Destry(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [Card.ACTION, Card.ATTACK, Card.KNIGHT]
        self.base = Game.DARKAGES
        self.name = "Sir Destry"
        self.desc = """+2 Cards. Each other player reveals the top 2 cards of his deck,
        trashes one of them costing from 3 to 6, and discards the rest.
        If a Knight is trashed by this, trash this card."""
        self.cards = 2
        self.cost = 5

    def special(self, game, player):
        self.knight_special(game, player)


###############################################################################
class Test_Sir_Destry(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Knight'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Sir Destry':
                break

    def test_score(self):
        """ Play the Sir"""
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import Game
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Dame_Molly(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [Card.ACTION, Card.ATTACK, Card.KNIGHT]
        self.base = Game.DARKAGES
        self.name = "Dame Molly"
        self.desc = """+2 Actions
        Each other player reveals the top 2 cards of his deck, trashes
        one of them costing from 3 to 6, and discards the rest.
        If a Knight is trashed by this, trash this card."""
        self.actions = 2
        self.cost = 5

    def special(self, game, player):
        self.knight_special(game, player)


###############################################################################
class Test_Dame_Molly(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Knight'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Dame Molly':
                break

    def test_score(self):
        """ Play the Dame"""
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

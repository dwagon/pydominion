#!/usr/bin/env python

import unittest
import Game
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Sir_Bailey(KnightCard):
    def __init__(self):
        super(Card_Sir_Bailey, self).__init__()
        self.cardtype = [Card.ACTION, Card.ATTACK, Card.KNIGHT]
        self.base = Game.DARKAGES
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Knight'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Sir Bailey':
                break

    def test_score(self):
        """ Play the Sir"""
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

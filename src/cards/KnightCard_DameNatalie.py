#!/usr/bin/env python

import unittest
import Game
import Card
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Dame_Natalie(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_KNIGHT]
        self.base = Game.DARKAGES
        self.name = "Dame Natalie"
        self.desc = """You may gain a card costing up to 3.
        Each other player reveals the top 2 cards of his deck, trashes one of them
        costing from 3 to 6, and discards the rest.
        If a Knight is trashed by this, trash this card."""
        self.cost = 5

    def special(self, game, player):
        player.plrGainCard(3)
        self.knight_special(game, player)


###############################################################################
class Test_Dame_Natalie(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Knight'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Dame Natalie':
                break

    def test_score(self):
        """ Play the Dame"""
        self.plr.test_input = ['get silver']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_discard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

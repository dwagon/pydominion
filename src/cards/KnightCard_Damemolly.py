#!/usr/bin/env python

import unittest
from Card import Card
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Dame_Molly(KnightCard):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'knight']
        self.base = 'darkages'
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
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Knight'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Dame Molly':
                break

    def test_score(self):
        """ Play the Dame"""
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

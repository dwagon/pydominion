#!/usr/bin/env python

import unittest
from Card import Card
from cards.Card_Knight import KnightCard


###############################################################################
class Card_Dame_Anna(KnightCard):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'attack', 'knight']
        self.base = 'darkages'
        self.name = "Dame Anna"
        self.desc = """You may trash up to 2 cards from your hand.
        Each other player reveals the top 2 cards of his deck, trashes one of them
        costing from 3 to 6, and discards the rest.
        If a Knight is trashed by this, trash this card."""
        self.cost = 5

    def special(self, game, player):
        for i in range(2):
            player.plrTrashCard()
        self.knight_special(game, player)


###############################################################################
class Test_Dame_Anna(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Knight'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        while True:
            self.card = self.g['Knight'].remove()
            if self.card.name == 'Dame Anna':
                break

    def test_score(self):
        """ Play the Dame"""
        tsize = self.g.trashSize()
        self.plr.setHand('Duchy', 'Province')
        self.plr.test_input = ['duchy', 'province', 'finish']
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize + 2)
        self.assertIsNotNone(self.g.inTrash('Province'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

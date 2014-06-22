#!/usr/bin/env python

import unittest
from Card import Card


class Card_Warehouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'TODO'
        self.desc = "+3 cards, +1 action, discard 3 cards"
        self.name = 'Warehouse'
        self.cards = 3
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """ Discard 3 cards"""
        player.plrDiscardCards(3)


###############################################################################
class Test_Warehouse(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['warehouse'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['warehouse'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a warehouse """
        self.plr.test_input = ['1', '2', '3', '0']
        self.plr.playCard(self.card)
        self.assertEquals(len(self.plr.hand), 5 - 3 + 3)
        self.assertEquals(self.plr.t['actions'], 1)
        self.assertEquals(len(self.plr.discardpile), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

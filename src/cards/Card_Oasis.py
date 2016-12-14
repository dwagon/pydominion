#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Oasis(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = "+1 card, +1 action, +1 coin, discard 1 card"
        self.name = 'Oasis'
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 3

    def special(self, game, player):
        """ Discard a card"""
        player.plrDiscardCards()


###############################################################################
class Test_Oasis(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Oasis'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Oasis'].remove()
        self.plr.setHand('Gold', 'Copper', 'Copper', 'Copper', 'Copper')
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play an oasis """
        self.plr.test_input = ['discard gold', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Market(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 cards, +1 action, +1 coin, +1 buys"
        self.name = 'Market'
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.coin = 1
        self.cost = 5


###############################################################################
class Test_Market(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Market'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Market'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a market """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

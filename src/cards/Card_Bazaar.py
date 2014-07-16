#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Bazaar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 cards, +2 action, +1 coin"
        self.name = 'Bazaar'
        self.cards = 1
        self.actions = 2
        self.coin = 1
        self.cost = 5


###############################################################################
class Test_Bazaar(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['bazaar'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['bazaar'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play Bazaar """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Workersvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 actions, +1 buy"
        self.name = "Worker's Village"
        self.cost = 4
        self.cards = 1
        self.actions = 2
        self.buys = 1


###############################################################################
class Test_Workersvillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['workersvillage'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['workersvillage'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play Workers Village """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

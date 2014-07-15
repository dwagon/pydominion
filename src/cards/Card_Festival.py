#!/usr/bin/env python

import unittest
from Card import Card


class Card_Festival(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+2 actions, +1 buys, +2 coin"
        self.name = 'Festival'
        self.actions = 2
        self.buys = 1
        self.coin = 2
        self.cost = 5


###############################################################################
class Test_Festival(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['festival'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['festival'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

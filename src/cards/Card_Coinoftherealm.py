#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Coinoftherealm(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['treasure', 'reserve']
        self.base = Game.ADVENTURE
        self.desc = "+1 Coin; Call for +2 Actions"
        self.name = 'Coin of the Realm'
        self.coin = 1
        self.cost = 2
        self.when = 'postaction'

    def hook_call_reserve(self, game, player):
        """ Directly after resolving an action you may call this for +2 Actions """
        player.addActions(2)


###############################################################################
class Test_Coinoftherealm(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Coin of the Realm'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Coin of the Realm'].remove()

    def test_play(self):
        """ Play a coin of the realm """
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.reserveSize(), 1)
        c = self.plr.in_reserve('Coin of the Realm')
        self.assertEqual(c.name, 'Coin of the Realm')

    def test_call(self):
        """ Call from Reserve"""
        self.plr.actions = 0
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        c = self.plr.call_reserve('Coin of the Realm')
        self.assertEqual(c.name, 'Coin of the Realm')
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

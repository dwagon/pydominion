#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Candlestickmaker(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = "+1 action, +1 buy, +1 coin token"
        self.name = 'Candlestick maker'
        self.actions = 1
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        """ Take a Coin Token """
        player.gainCoins(1)


###############################################################################
class Test_Candlestickmaker(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['candlestickmaker'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['candlestickmaker'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a candlestick maker """
        self.plr.coins = 0
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.coins, 1)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.plr.t['buys'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

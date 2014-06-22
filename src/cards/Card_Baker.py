#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Baker(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = "+1 card, +1 action, +1 coin token"
        self.name = 'Baker'
        self.actions = 1
        self.cards = 1
        self.cost = 5

    def special(self, game, player):
        """ Take a Coin Token """
        player.gainCoins(1)

    def setup(self, game):
        """ Each Player takes a coin token"""
        for plr in game.players.values():
            plr.gainCoins(1)


###############################################################################
class Test_Baker(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['baker'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['baker'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_setup(self):
        """ Test each player having a coin """
        self.assertEqual(self.plr.coins, 1)

    def test_play(self):
        """ Play a baker """
        self.plr.coins = 0
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.coins, 1)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(len(self.plr.hand), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

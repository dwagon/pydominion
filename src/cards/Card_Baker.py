#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Baker(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'guilds'
        self.desc = "+1 card, +1 action, +1 special coin"
        self.name = 'Baker'
        self.actions = 1
        self.cards = 1
        self.cost = 5

    def special(self, game, player):
        """ Take a Coin Token """
        player.gainSpecialCoins(1)

    def setup(self, game):
        """ Each Player takes a coin token"""
        for plr in game.playerList():
            plr.gainSpecialCoins(1)


###############################################################################
class Test_Baker(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Baker'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Baker'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_setup(self):
        """ Test each player having a coin """
        self.assertEqual(self.plr.getSpecialCoins(), 1)

    def test_play(self):
        """ Play a baker """
        self.plr.specialcoins = 0
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getSpecialCoins(), 1)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

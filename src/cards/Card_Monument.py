#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Monument(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "+2 coin, +1 VP"
        self.name = 'Monument'
        self.cost = 4
        self.coin = 2

    def special(self, game, player):
        player.addScore('Monument', 1)


###############################################################################
class Test_Monument(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Monument'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Monument'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Monument'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

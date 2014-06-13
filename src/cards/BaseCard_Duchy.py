#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Duchy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'dominion'
        self.desc = "3 VP"
        self.playable = False
        self.basecard = True
        self.name = 'Duchy'
        self.cost = 5
        self.victory = 3


###############################################################################
class Test_Duchy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1)
        self.plr = self.g.players[0]
        self.card = self.g['duchy'].remove()

    def test_have(self):
        self.plr.addCard(self.card)
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Duchy'], 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Colony(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'prosperity'
        self.desc = "+10 VP"
        self.basecard = True
        self.name = 'Colony'
        self.playable = False
        self.cost = 11
        self.victory = 10


###############################################################################
class Test_Colony(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, prosperity=True)
        self.g.startGame(numplayers=1)
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['colony'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_score(self):
        """ Score a colony """
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Colony'], 10)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Duke(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'victory'
        self.base = 'intrigue'
        self.desc = "Worth 1 per duchy"
        self.name = 'Duke'
        self.playable = False
        self.cost = 5

    def special_score(self, game, player):
        """ Worth 1VP per Duchy you have"""
        vp = 0
        for c in player.allCards():
            if c.cardname == 'duchy':
                vp += 1
        return vp


###############################################################################
class Test_Duke(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['duke'])
        self.plr = self.g.playerList(0)

    def test_score(self):
        self.plr.setDeck('duchy', 'duchy', 'estate')
        self.plr.setHand('silver')
        self.plr.setDiscard('duke')
        sc = self.plr.getScore()
        self.assertEqual(sc, 9)     # 3 per duchy, 1 per estate, 2 from duke


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

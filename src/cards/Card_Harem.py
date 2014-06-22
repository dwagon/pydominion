#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Harem(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'intrigue'
        self.desc = "+2 Gold; 2 VPs"
        self.name = 'Harem'
        self.gold = 2
        self.victory = 2
        self.cost = 6


###############################################################################
class Test_Harem(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['harem'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['harem'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Harem """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getGold(), 2)

    def test_score(self):
        """ Score the harem """
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Harem'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

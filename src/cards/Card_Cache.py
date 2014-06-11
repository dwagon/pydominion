#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Cache(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.desc = "+3 gold. Gain two coppers when you gain this"
        self.name = 'Cache'
        self.cost = 5
        self.gold = 3

    def hook_gainThisCard(self, game, player):
        """ When you gain this, gain two Coppers"""
        player.output("Gained 2 copper from cache")
        for i in range(2):
            player.gainCard('Copper')


###############################################################################
class Test_Cache(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['cache'])
        self.plr = self.g.players.values()[0]
        self.cache = self.g['cache'].remove()

    def test_gain(self):
        self.plr.gainCard('cache')
        sdp = sorted([c.name for c in self.plr.discardpile])
        self.assertEqual(sorted(['Copper', 'Copper', 'Cache']), sdp)

    def test_play(self):
        self.plr.addCard(self.cache, 'hand')
        self.plr.playCard(self.cache)
        self.assertEqual(self.plr.t['gold'], 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

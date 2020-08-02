#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Cache(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.name = 'Cache'
        self.cost = 5
        self.coin = 3

    def desc(self, player):
        if player.phase == "buy":
            return "+3 coin. Gain two coppers when you gain this"
        return "+3 coin"

    def hook_gain_this_card(self, game, player):
        """ When you gain this, gain two Coppers"""
        player.output("Gained 2 copper from cache")
        for _ in range(2):
            player.gainCard('Copper')
        return {}


###############################################################################
class Test_Cache(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Cache'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.cache = self.g['Cache'].remove()

    def test_gain(self):
        self.plr.gainCard('Cache')
        sdp = sorted([c.name for c in self.plr.discardpile])
        self.assertEqual(sorted(['Copper', 'Copper', 'Cache']), sdp)

    def test_play(self):
        self.plr.addCard(self.cache, 'hand')
        self.plr.playCard(self.cache)
        self.assertEqual(self.plr.getCoin(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Copper(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = 'dominion'
        self.basecard = True
        self.playable = False
        self.callable = False
        self.desc = "+1 coin"
        self.name = 'Copper'
        self.coin = 1
        self.cost = 0

    def calc_numcards(self, game):
        return 60 - game.numplayers * 7


###############################################################################
class Test_Copper(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Copper'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

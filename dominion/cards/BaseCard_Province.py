#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Province(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.DOMINION
        self.desc = "6 VP"
        self.playable = False
        self.basecard = True
        self.name = "Province"
        self.cost = 8
        self.victory = 6

    def calc_numcards(self, game):
        if game.numplayers == 2:
            return 8
        if game.numplayers > 4:
            return 3 * game.numplayers
        return 12


###############################################################################
class Test_Province(unittest.TestCase):
    def setUp(self):
        pass

    def test_two_player(self):
        self.g = Game.Game(quiet=True, numplayers=2)
        self.g.start_game()
        self.assertEqual(self.g["Province"].pilesize, 8)
        self.plr = self.g.player_list()[0]

    def Xtest_five(self):
        self.g = Game.Game(quiet=True, numplayers=5)
        self.g.start_game()
        self.assertEqual(self.g["Province"].pilesize, 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

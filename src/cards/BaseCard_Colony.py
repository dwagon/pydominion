#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Colony(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.VICTORY
        self.base = Game.PROSPERITY
        self.desc = "+10 VP"
        self.basecard = True
        self.name = 'Colony'
        self.playable = False
        self.cost = 11
        self.victory = 10

    def calc_numcards(self, game):
        if game.numplayers == 2:
            return 8
        return 12


###############################################################################
class Test_Colony(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, prosperity=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Colony'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_score(self):
        """ Score a colony """
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Colony'], 10)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

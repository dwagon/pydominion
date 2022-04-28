#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Copper(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.DOMINION
        self.basecard = True
        self.playable = False
        self.callable = False
        self.desc = "+1 coin"
        self.name = "Copper"
        self.coin = 1
        self.cost = 0

    @classmethod
    def calc_numcards(cls, game):
        return 60


###############################################################################
class Test_Copper(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Copper"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

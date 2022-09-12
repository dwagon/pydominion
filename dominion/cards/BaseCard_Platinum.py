#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Platinum(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = "+5 coin"
        self.name = "Platinum"
        self.playable = False
        self.basecard = True
        self.coin = 5
        self.cost = 9
        self.numcards = 12


###############################################################################
class Test_Platinum(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, prosperity=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Platinum"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a platinum"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

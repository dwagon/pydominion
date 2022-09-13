#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Plunder(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.EMPIRES
        self.desc = """+2 Coin, +1VP"""
        self.name = "Plunder"
        self.coin = 2
        self.victory = 1
        self.cost = 5


###############################################################################
class Test_Plunder(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Plunder"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Plunder"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a rebuild"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.get_score_details()["Plunder"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

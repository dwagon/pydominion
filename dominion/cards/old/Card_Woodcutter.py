#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Woodcutter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+1 buys, +2 coin"
        self.name = "Woodcutter"
        self.buys = 1
        self.coin = 2
        self.cost = 3


###############################################################################
class Test_Woodcutter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Woodcutter"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Woodcutter"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play the woodcutter"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.getBuys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

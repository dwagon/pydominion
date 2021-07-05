#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Workersvillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.PROSPERITY
        self.desc = "+1 card, +2 actions, +1 buy"
        self.name = "Worker's Village"
        self.cost = 4
        self.cards = 1
        self.actions = 2
        self.buys = 1


###############################################################################
class Test_Workersvillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Worker's Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Worker's Village"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play Workers Village"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.hand.size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

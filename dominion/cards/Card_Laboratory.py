#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Laboratory(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "+2 cards, +1 action"
        self.name = "Laboratory"
        self.cards = 2
        self.actions = 1
        self.cost = 5


###############################################################################
class Test_Laboratory(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Laboratory"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Laboratory"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Laboratory"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        # 5 hand, +2 for playing lab
        self.assertEqual(self.plr.hand.size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

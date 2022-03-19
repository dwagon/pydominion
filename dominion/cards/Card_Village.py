#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Village(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+1 cards, +2 actions"
        self.name = "Village"
        self.cards = 1
        self.actions = 2
        self.cost = 3


###############################################################################
class Test_Village(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Village"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the village"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

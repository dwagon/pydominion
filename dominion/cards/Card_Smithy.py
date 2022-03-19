#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Smithy(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = "+3 cards"
        self.name = "Smithy"
        self.cards = 3
        self.cost = 4


###############################################################################
class Test_Smithy(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Smithy"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Smithy"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play the smithy"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

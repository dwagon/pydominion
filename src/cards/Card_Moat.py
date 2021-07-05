#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Moat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.DOMINION
        self.desc = "+2 cards, defense"
        self.name = "Moat"
        self.defense = True
        self.cost = 2
        self.cards = 2


###############################################################################
class Test_Moat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play a moat"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

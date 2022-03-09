#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Underling(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LIAISON]
        self.base = Game.ALLIES
        self.name = "Underling"
        self.cards = 1
        self.actions = 1
        self.favors = 1
        self.desc = "+1 Card; +1 Action; +1 Favor"
        self.cost = 3


###############################################################################
class Test_Underling(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Underling"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play the card"""
        favs = self.plr.getFavor()
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getFavor(), favs + 1)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

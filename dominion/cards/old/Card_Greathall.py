#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Greathall(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_VICTORY]
        self.base = Game.INTRIGUE
        self.desc = "+1 card, +1 action, 1VP"
        self.name = "Great Hall"
        self.cost = 3
        self.cards = 1
        self.actions = 1

    def special_score(self, game, player):
        return 1


###############################################################################
class Test_Greathall(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Great Hall"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Great Hall"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a Great Hall"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_score(self):
        """Have a victory point just for existing"""
        score = self.plr.get_score_details()
        self.assertEqual(score["Great Hall"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

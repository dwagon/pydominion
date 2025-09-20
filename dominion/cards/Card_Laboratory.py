#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles


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
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Laboratory")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a Laboratory"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        # 5 hand, +2 for playing lab
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

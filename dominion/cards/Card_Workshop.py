#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Workshop(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Gain a card costing up to 4"
        self.name = "Workshop"
        self.cost = 3

    def special(self, game, player):
        """Gain a card costing up to 4"""
        player.plr_gain_card(4)


###############################################################################
class TestWorkshop(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["Workshop", "Gardens"],
            badcards=["Blessed Village", "Cemetery"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.workshop = self.g.get_card_from_pile("Workshop")
        self.plr.add_card(self.workshop, Piles.HAND)

    def test_gain_zero(self):
        self.plr.test_input = ["Finish"]
        self.plr.play_card(self.workshop)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 0)

    def test_gain_one(self):
        self.plr.test_input = ["Get Gardens"]
        self.plr.play_card(self.workshop)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertLessEqual(self.plr.piles[Piles.DISCARD][0].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

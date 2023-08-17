#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Expand(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "Trash a card from hand and gain one costing 3 more"
        self.name = "Expand"
        self.cost = 7

    def special(self, game, player):
        """Trash a card from your hand. Gain a card costing up to
        3 more than the trashed card"""
        tc = player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from your hand. Gain another costing up to 3 more than the one you trashed",
        )
        if tc:
            cost = tc[0].cost
            player.plr_gain_card(cost + 3)


###############################################################################
class Test_Expand(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Expand"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.expand = self.g["Expand"].remove()

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.add_card(self.expand, Piles.HAND)
        self.plr.test_input = ["Trash Copper", "Get Estate"]
        self.plr.play_card(self.expand)
        self.g.print_state()
        self.assertTrue(self.plr.piles[Piles.HAND].is_empty())
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertLessEqual(self.plr.piles[Piles.DISCARD][0].cost, 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

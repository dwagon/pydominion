#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Upgrade(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+1 Card, +1 Action. Trash a card from your hand. Gain a card costing exactly 1 more than it."
        self.name = "Upgrade"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """Trash a card from your hand. Gain a card costing up to 1 more than it"""
        tc = player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from your hand. Gain a card costing exactly 1 more than it",
        )
        if tc:
            cost = player.card_cost(tc[0])
            player.plr_gain_card(cost + 1, "equal")


###############################################################################
class Test_Upgrade(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Upgrade"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Upgrade")

    def test_play(self):
        """Play the Upgrade"""
        tsize = self.g.trash_pile.size()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_trash(self):
        """Trash an upgrade"""
        tsize = self.g.trash_pile.size()
        self.plr.piles[Piles.HAND].set("Duchy", "Copper")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Duchy", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.g.trash_pile.size(), tsize + 1)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

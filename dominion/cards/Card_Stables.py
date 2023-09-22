#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Stables(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """You may discard a Treasure. If you do, +3 Cards and +1 Action."""
        self.name = "Stables"
        self.cost = 5

    def special(self, game, player):
        treasures = [c for c in player.piles[Piles.HAND] if c.isTreasure()]
        tr = player.plr_discard_cards(
            cardsrc=treasures, prompt="Discard a card and get +3 Cards +1 Action"
        )
        if tr:
            player.add_actions(1)
            player.pickup_cards(3)


###############################################################################
class Test_Stables(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Stables"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Stables")

    def test_play(self):
        """Play duchess - keep on deck"""
        self.plr.piles[Piles.HAND].set("Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["silver"]
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

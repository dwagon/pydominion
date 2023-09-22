#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Warehouse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "+3 cards, +1 action, discard 3 cards"
        self.name = "Warehouse"
        self.cards = 3
        self.actions = 1
        self.cost = 3

    def special(self, game, player):
        """Discard 3 cards"""
        player.plr_discard_cards(3, force=True)


###############################################################################
class Test_Warehouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Warehouse"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Warehouse")

    def test_playcard(self):
        """Play a warehouse"""
        self.plr.piles[Piles.HAND].set("Estate", "Copper", "Silver", "Gold")
        self.plr.piles[Piles.DECK].set("Province", "Province", "Province", "Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = [
            "discard estate",
            "discard copper",
            "discard duchy",
            "finish",
        ]
        self.plr.play_card(self.card)
        # Initial hand size - 3 discards + 3 pickups - 1 played
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 - 3 + 3 - 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

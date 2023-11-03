#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Old_Map"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Old_Map(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ODYSSEY]
        self.base = Card.CardExpansion.ALLIES
        self.cost = 3
        self.name = "Old Map"
        self.cards = 1
        self.actions = 1
        self.desc = """+1 Card; +1 Action; Discard a card. +1 Card. You may rotate the Odysseys."""
        self.pile = "Odysseys"

    def special(self, game, player):
        player.plr_discard_cards(num=1)
        player.pickup_cards(1)
        if opt := player.plr_choose_options(
            "Do you want to rotate the Odysseys?",
            ("Don't change", False),
            ("Rotate", True),
        ):
            game.card_piles["Odysseys"].rotate()


###############################################################################
class TestOldMap(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Odysseys", "Old Map")

    def test_play(self):
        """Play the card"""
        self.plr.piles[Piles.DECK].set("Estate", "Duchy", "Province")
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Discard Copper", "Rotate"]
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Copper", self.plr.piles[Piles.HAND])
        self.assertIn("Province", self.plr.piles[Piles.HAND])
        self.assertEqual(self.g.card_piles["Odysseys"].top_card(), "Voyage")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

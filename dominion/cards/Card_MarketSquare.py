#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_MarketSquare(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.REACTION]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """+1 Card, +1 Action, +1 Buy.
        When one of your cards is trashed, you may discard this from your hand. If you do, gain a Gold."""
        self.name = "Market Square"
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.cost = 3

    def hook_trash_card(self, game, player, card):
        """This should only activate if Market Square is in the hand"""
        if self.location != Piles.HAND:
            return
        gold = player.plr_choose_options(
            "Discard Market Square to gain a Gold?",
            ("Keep Market Square in hand", False),
            ("Discard and gain a Gold", True),
        )
        if gold:
            player.discard_card(self)
            player.gain_card("Gold")


###############################################################################
class TestMarketSquare(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Market Square"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Market Square")

    def test_play(self):
        """Play the card"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_trash_and_keep(self):
        """Choose to keep MS after a trash"""
        self.plr.piles[Piles.HAND].set("Copper", "Market Square")
        self.plr.test_input = ["keep"]
        self.plr.trash_card(self.plr.piles[Piles.HAND]["Copper"])
        self.assertIn("Market Square", self.plr.piles[Piles.HAND])

    def test_trash_and_discard(self):
        """Choose to keep MS after a trash"""
        self.plr.piles[Piles.HAND].set("Copper", "Market Square")
        self.plr.test_input = ["discard"]
        self.plr.trash_card(self.plr.piles[Piles.HAND]["Copper"])
        self.assertNotIn("Market Square", self.plr.piles[Piles.HAND])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])

    def test_trash_in_played(self):
        """Test trashing a card with MS not in hand"""
        self.plr.piles[Piles.HAND].set("Copper")
        self.plr.piles[Piles.PLAYED].set("Market Square")
        self.plr.trash_card(self.plr.piles[Piles.HAND]["Copper"])
        self.g.print_state()
        self.assertNotIn("Gold", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Capital_City(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.cards = 1
        self.actions = 2
        self.name = "Capital City"
        self.desc = """+1 Card; +2 Actions; You may discard 2 cards for +$2.;
            You may pay $2 for +2 Cards."""
        self.cost = 5

    def special(self, game, player):
        ch1 = player.plr_choose_options(
            "Discard 2 cards to gain $2 coin?",
            ("Do nothing", False),
            ("Discard 2 Cards", True),
        )
        if ch1:
            discard = player.plr_discard_cards(num=2)
            if len(discard) == 2:
                player.coins.add(2)
        if player.coins.get() >= 2:
            ch2 = player.plr_choose_options(
                "Pay $2 to gain 2 cards?",
                ("Do nothing", False),
                ("Gain 2 Cards", True),
            )
            if ch2:
                player.coins.add(-2)
                player.pickup_cards(2)


###############################################################################
class Test_Capital_City(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Capital City"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Capital City"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.hand.set("Copper", "Copper", "Estate", "Duchy")
        self.plr.deck.set("Gold", "Silver", "Copper", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = [
            "Discard",
            "Discard Estate",
            "Discard Duchy",
            "Finish",
            "Gain",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.hand.size(), 4 + 1 - 2 + 2)
        self.assertNotIn("Duchy", self.plr.hand)
        self.assertIn("Silver", self.plr.hand)

    def test_play_no_pickup(self):
        """Play the card but don't pickup new cards"""
        self.plr.hand.set("Copper", "Copper", "Estate", "Duchy")
        self.plr.deck.set("Gold", "Silver", "Copper", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = [
            "Discard",
            "Discard Estate",
            "Discard Duchy",
            "Finish",
            "nothing",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.hand.size(), 4 + 1 - 2)
        self.assertNotIn("Duchy", self.plr.hand)
        self.assertNotIn("Silver", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

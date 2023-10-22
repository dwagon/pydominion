#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Souk"""

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Souk(Card.Card):
    """Souk"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """+1 Buy; +$7; –$1 per card in your hand (you can't go below $0).
        When you gain this, trash up to 2 cards from your hand."""
        self.buys = 1
        self.name = "Souk"
        self.cost = 7

    def hook_this_card_cost(self, game, player):
        """–$1 per card in your hand."""
        return -len(player.piles[Piles.HAND])

    def hook_gain_this_card(self, game, player):
        """When you gain this, trash up to 2 cards from your hand."""
        player.plr_trash_card(num=2)


###############################################################################
class Test_Souk(unittest.TestCase):
    """Test Souk"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Souk", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Souk")

    def test_play(self):
        """Play a card"""
        buys = self.plr.buys.get()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), buys + 1)

    def test_gain_card(self):
        """Gain the card"""
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold", "Estate")
        self.plr.test_input = ["Trash Copper", "Trash Silver", "Finish"]
        self.plr.gain_card("Souk")
        self.assertIn("Silver", self.g.trash_pile)
        self.assertIn("Copper", self.g.trash_pile)

    def test_cost(self):
        """Cost of card"""
        self.plr.piles[Piles.HAND].empty()
        self.assertEqual(self.plr.card_cost(self.card), 7)
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Gold")
        self.assertEqual(self.plr.card_cost(self.card), 7 - 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

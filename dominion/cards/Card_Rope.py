#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Rope"""

import unittest
from typing import Optional

from dominion import Game, Card, Piles


###############################################################################
class Card_Rope(Card.Card):
    """Rope"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.DURATION]
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "$1; +1 Buy; At the start of your next turn, +1 Card and you may trash a card from your hand."
        self.coin = 1
        self.buys = 1
        self.name = "Rope"
        self.cost = 4

    def duration(self, game, player):
        """At the start of your next turn, +1 Card and you may trash a card from your hand."""
        player.pickup_cards(1)
        player.plr_trash_card(num=1)


###############################################################################
class Test_Rope(unittest.TestCase):
    """Test Rope"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Rope"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Rope")

    def test_play_card(self):
        """Play a card"""
        self.plr.add_card(self.card, Piles.HAND)
        coins = self.plr.coins.get()
        buys = self.plr.buys.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 1)
        self.assertEqual(self.plr.buys.get(), buys + 1)

    def test_duration(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.plr.test_input = ["Silver"]
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Duchy")
        self.plr.start_turn()
        self.assertIn("Silver", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

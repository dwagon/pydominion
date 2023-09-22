#!/usr/bin/env python

import unittest
import dominion.Card as Card
from dominion import Game, Card, Piles


###############################################################################
class Card_Remake(Card.Card):
    """Remake"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = "Do this twice: Trash a card from your hand, then gain a card costing exactly 1 more than the trashed card."
        self.name = "Remake"
        self.cost = 4

    def special(self, game, player):
        for _ in range(2):
            c = player.plr_trash_card(prompt="Trash a card and gain one costing 1 more")
            if c:
                player.plr_gain_card(cost=c[0].cost + 1, modifier="equal")


###############################################################################
class Test_Remake(unittest.TestCase):
    """Test Remake"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Remake", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Remake")

    def test_playcard(self):
        """Play a remake"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = [
            "Trash Estate",
            "Get Silver",
            "Trash Copper",
            "Finish Selecting",
        ]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()


# EOF

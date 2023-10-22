#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Shantytown(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+2 actions. If no action in hand, +2 cards"
        self.name = "Shanty Town"
        self.actions = 2
        self.cost = 3

    def special(self, game, player):
        """Reveal your hand. If you have no Action cards in hand, +2 cards"""
        for c in player.piles[Piles.HAND]:
            player.reveal_card(c)
            if c.isAction():
                break
        else:
            player.output("No actions - picking up 2 cards")
            player.pickup_cards(2)


###############################################################################
class Test_Shantytown(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Shanty Town", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Shanty Town")

    def test_no_actions(self):
        """Test Shany Town with no actions"""
        self.plr.piles[Piles.HAND].set("Estate", "Estate", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3 + 2)

    def test_actions(self):
        """Test Shany Town with actions"""
        self.plr.piles[Piles.HAND].set("Moat", "Estate", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

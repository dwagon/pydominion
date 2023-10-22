#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Salvager(Card.Card):
    """Salvager"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.SEASIDE
        self.desc = """+1 Buy. Trash a card from your hand. Gain Coins equal to its cost."""
        self.name = "Salvager"
        self.buys = 1
        self.cost = 4

    def special(self, game, player):
        card = player.plr_trash_card(force=True)
        player.output(f"Gained {card[0].cost} coin")
        player.coins.add(card[0].cost)


###############################################################################
class Test_Salvager(unittest.TestCase):
    """Test Salvager"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Salvager"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Salvager")

    def test_play(self):
        """Play a salvage"""
        self.plr.piles[Piles.HAND].set("Duchy", "Estate")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["duchy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertIn("Duchy", self.g.trash_pile)
        self.assertEqual(self.plr.coins.get(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

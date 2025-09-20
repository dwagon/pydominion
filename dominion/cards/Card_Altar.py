#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Altar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Trash a card from your hand. Gain a card costing up to 5 Coin."""
        self.name = "Altar"
        self.cost = 6

    def special(self, game, player):
        # Trash a card from your hand
        player.plr_trash_card(prompt="Trash a card from your hand", force=True)

        # Gain a card costing up to 5 Coin
        player.plr_gain_card(5)


###############################################################################
class Test_Altar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Altar", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Altar")

    def test_play(self):
        """Play an Altar"""
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Province", "Moat"]
        self.plr.play_card(self.card)
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Province", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fugitive(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.TRAVELLER]
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Action, +2 Cards; Discard a card"
        self.name = "Fugitive"
        self.purchasable = False
        self.actions = 1
        self.cards = 2
        self.cost = 4
        self.numcards = 5

    def special(self, game, player):
        player.plr_discard_cards(num=1)

    def hook_discard_this_card(self, game, player, source):
        """Replace with Warrior"""
        player.replace_traveller(self, "Disciple")


###############################################################################
class Test_Fugitive(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Fugitive"].remove()

    def test_fugitive(self):
        """Play a fugitive"""
        self.plr.piles[Piles.HAND].set("Province")
        self.plr.test_input = ["province"]
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 1)
        self.assertIn("Province", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

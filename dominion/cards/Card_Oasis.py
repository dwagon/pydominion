#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles


###############################################################################
class Card_Oasis(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = "+1 card, +1 action, +1 coin, discard 1 card"
        self.name = "Oasis"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 3

    def special(self, game, player):
        """Discard a card"""
        player.plr_discard_cards()


###############################################################################
class Test_Oasis(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Oasis"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Oasis")
        self.plr.piles[Piles.HAND].set("Gold", "Copper", "Copper", "Copper", "Copper")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play an oasis"""
        self.plr.test_input = ["discard gold", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Galleria(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ALLIES
        self.name = "Galleria"
        self.coin = 3
        self.desc = "+$3; This turn, when you gain a card costing $3 or $4, +1 Buy."
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if card.cost in (3, 4):
            player.buys.add(1)


###############################################################################
class Test_Galleria(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Galleria"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Galleria"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        coins = self.plr.coins.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), coins + 3)

    def test_gain(self):
        """Gain a card"""
        buys = self.plr.buys.get()
        self.plr.gain_card("Silver")
        self.assertEqual(self.plr.buys.get(), buys + 1)

    def test_no_gain(self):
        """Gain a card that doesn't cost correctly"""
        buys = self.plr.buys.get()
        self.plr.gain_card("Copper")
        self.assertEqual(self.plr.buys.get(), buys)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

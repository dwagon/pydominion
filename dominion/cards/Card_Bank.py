#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


class Card_Bank(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 Coin per treasure in play"
        self.name = "Bank"
        self.cost = 7

    def hook_coinvalue(self, game, player):
        """When you play this it is worth 1 per treasure card you
        have in play (counting this)"""
        num_treas = sum([1 for c in player.piles[Piles.PLAYED] if c.isTreasure()])
        return num_treas


###############################################################################
class Test_Bank(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bank"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Bank")
        self.plr.add_card(self.card, Piles.HAND)

    def test_gainnothing(self):
        self.plr.piles[Piles.PLAYED].set("Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_gainsomething(self):
        self.plr.piles[Piles.PLAYED].set("Copper", "Silver", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

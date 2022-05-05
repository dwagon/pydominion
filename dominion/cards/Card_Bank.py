#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


class Card_Bank(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = "+1 Coin per treasure in play"
        self.name = "Bank"
        self.cost = 7

    def hook_coinvalue(self, game, player):
        """When you play this it is worth 1 per treasure card you
        have in play (counting this)"""
        num_treas = sum([1 for c in player.played if c.isTreasure()])
        return num_treas


###############################################################################
class Test_Bank(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bank"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Bank"].remove()
        self.plr.add_card(self.card, "hand")

    def test_gainnothing(self):
        self.plr.played.set("Estate", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)

    def test_gainsomething(self):
        self.plr.played.set("Copper", "Silver", "Estate")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

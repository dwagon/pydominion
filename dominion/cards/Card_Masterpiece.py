#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Masterpiece(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.GUILDS
        self.name = "Masterpiece"
        self.overpay = True
        self.coin = 1
        self.cost = 3

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """+1 Coin. When you buy this, you may overpay for it.
                If you do, gain a Silver per coin you overpaid."""
        return "+1 Coin"

    def hook_overpay(self, game, player, amount):
        player.output("Gained %d Silvers" % amount)
        for _ in range(amount):
            player.gain_card("Silver")


###############################################################################
class TestMasterpiece(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Masterpiece"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Masterpiece"].remove()

    def test_play(self):
        """Play a Masterpiece"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_buy(self):
        """Buy a Masterpiece"""
        self.plr.coins.set(5)
        self.plr.test_input = ["1"]
        self.plr.buy_card("Masterpiece")
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

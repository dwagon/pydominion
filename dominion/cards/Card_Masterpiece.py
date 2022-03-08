#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Masterpiece(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.GUILDS
        self.name = "Masterpiece"
        self.overpay = True
        self.coin = 1
        self.cost = 3

    def desc(self, player):
        if player.phase == "buy":
            return """+1 Coin. When you buy this, you may overpay for it.
                If you do, gain a Silver per coin you overpaid."""
        return "+1 Coin"

    def hook_overpay(self, game, player, amount):
        player.output("Gained %d Silvers" % amount)
        for _ in range(amount):
            player.gainCard("Silver")


###############################################################################
class Test_Masterpiece(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Masterpiece"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Masterpiece"].remove()

    def test_play(self):
        """Play a Masterpiece"""
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_buy(self):
        """Buy a Masterpiece"""
        self.plr.coin = 5
        self.plr.test_input = ["1"]
        self.plr.buyCard(self.g["Masterpiece"])
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

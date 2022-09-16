#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Traderoute(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = (
            "+1 Buy; Trash a card from your hand. +1 Coin per Coin token on the Trade Route mat."
        )
        self.name = "Trade Route"
        self.cost = 3
        self.buys = 1

    @classmethod
    def setup(cls, game):
        """Setup: Add a Coin token to each Victory Supply pile; move that token
        to the Trade Route mat when a card is gained from the pile."""
        cls.tokens = {}
        cls.game = game
        for cp in list(game.cardpiles.values()):
            if cp.isVictory():
                cls.tokens[cp.name] = len(cp)

    def isWorth(self):
        worth = 0
        for cp in list(self.game.cardpiles.values()):
            if cp.name in self.tokens:
                if self.tokens[cp.name] != len(cp):
                    worth += 1
        return worth

    def special(self, game, player):
        """+1 coin per token on the trade route map. Trash a card
        from your hand. Setup: Put a token on each victory card
        supply pile. When a card is gained from that pile move the
        token to the trade route map"""
        player.plr_trash_card()
        player.coins.add(self.isWorth())


###############################################################################
class Test_Traderoute(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Trade Route"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.traderoute = self.g["Trade Route"].remove()
        self.plr.add_card(self.traderoute, "hand")

    def test_playZero(self):
        self.plr.test_input = ["finish selecting"]
        self.plr.play_card(self.traderoute)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_playOne(self):
        self.plr.test_input = ["finish selecting"]
        self.g["Estate"].remove()
        self.plr.play_card(self.traderoute)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_playTwo(self):
        self.plr.test_input = ["finish selecting"]
        self.g["Estate"].remove()
        self.g["Province"].remove()
        self.plr.play_card(self.traderoute)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

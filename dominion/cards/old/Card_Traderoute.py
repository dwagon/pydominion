#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_TradeRoute(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 Buy; Trash a card from your hand. +1 Coin per Coin token on the Trade Route mat."
        self.name = "Trade Route"
        self.cost = 3
        self.buys = 1

    @classmethod
    def setup(cls, game):
        """Setup: Add a Coin token to each Victory Supply pile; move that token
        to the Trade Route mat when a card is gained from the pile."""
        cls.tokens = {}
        cls.game = game
        for name, card_pile in game.card_piles():
            card = game.get_card_from_pile(name)
            if card.isVictory():
                cls.tokens[name] = len(card_pile)

    def is_worth(self, game):
        worth = 0
        for name, card_pile in game.card_piles():
            if name in self.tokens:
                if self.tokens[name] != len(card_pile):
                    worth += 1
        return worth

    def special(self, game, player):
        """+1 coin per token on the trade route map. Trash a card
        from your hand. Setup: Put a token on each victory card
        supply pile. When a card is gained from that pile move the
        token to the trade route map"""
        player.plr_trash_card()
        player.coins.add(self.is_worth(game))


###############################################################################
class TestTradeRoute(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Trade Route"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.trade_route = self.g["Trade Route"].remove()
        self.plr.add_card(self.trade_route, Piles.HAND)

    def test_playZero(self):
        self.plr.test_input = ["finish selecting"]
        self.plr.play_card(self.trade_route)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.buys.get(), 2)

    def test_playOne(self):
        self.plr.test_input = ["finish selecting"]
        self.g["Estate"].remove()
        self.plr.play_card(self.trade_route)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_playTwo(self):
        self.plr.test_input = ["finish selecting"]
        self.g["Estate"].remove()
        self.g["Province"].remove()
        self.plr.play_card(self.trade_route)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

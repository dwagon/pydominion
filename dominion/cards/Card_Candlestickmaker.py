#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Candlestickmaker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = "+1 action, +1 buy, +1 coffer"
        self.name = "Candlestick Maker"
        self.actions = 1
        self.buys = 1
        self.cost = 2

    def special(self, game, player):
        """Take a Coin Token"""
        player.coffers.add(1)


###############################################################################
class Test_Candlestickmaker(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Candlestick Maker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Candlestick Maker")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a candlestick maker"""
        self.plr.coffers.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coffers.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.buys.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

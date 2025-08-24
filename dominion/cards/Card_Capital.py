#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Capital(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+6 Coin, +1 Buy. When you discard this from play, take 6 Debt"
        self.name = "Capital"
        self.coin = 6
        self.buys = 1
        self.cost = 5

    def hook_discard_this_card(self, game, player, source):
        if source == "played":
            player.debt += 6
            player.payback()


###############################################################################
class Test_Capital(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Capital"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Capital")

    def test_play(self):
        """Play a Capital"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 6)
        self.plr.coins.set(3)
        self.plr.discard_card(self.card, Piles.PLAYED)
        self.assertEqual(self.plr.debt.get(), 3)
        self.assertEqual(self.plr.coins.get(), 0)

    def test_dontplay(self):
        """Dont play a Capital"""
        self.plr.add_card(self.card, Piles.HAND)
        self.assertEqual(self.plr.buys.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.plr.discard_card(self.card)
        self.assertEqual(self.plr.debt.get(), 0)
        self.assertEqual(self.plr.coins.get(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

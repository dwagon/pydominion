#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Capital(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.EMPIRES
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Capital"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Capital"].remove()

    def test_play(self):
        """Play a Capital"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.get_coins(), 6)
        self.plr.coin = 3
        self.plr.discard_card(self.card, "played")
        self.assertEqual(self.plr.debt, 3)
        self.assertEqual(self.plr.coin, 0)

    def test_dontplay(self):
        """Dont play a Capital"""
        self.plr.add_card(self.card, "hand")
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_coins(), 0)
        self.plr.discard_card(self.card)
        self.assertEqual(self.plr.debt, 0)
        self.assertEqual(self.plr.coin, 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

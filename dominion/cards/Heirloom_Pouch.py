#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Pouch(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_HEIRLOOM]
        self.base = Game.NOCTURNE
        self.desc = "+1 Coin, +1 Buy"
        self.name = "Pouch"
        self.cost = 2
        self.coin = 1
        self.buys = 1
        self.purchasable = False


###############################################################################
class Test_Pouch(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Tracker"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Pouch"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.buys = 0
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.get_buys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

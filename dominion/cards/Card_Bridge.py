#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bridge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "+1 Buy +1 Coin. All cards (including cards in players hands) cost 1 less this turn, but not less than 0."
        self.name = "Bridge"
        self.buys = 1
        self.coin = 1
        self.cost = 4

    def hook_cardCost(self, game, player, card):
        """All cards (including cards in players' hands) cost 1
        less this turn, but not less than 0"""
        if self in player.played:
            return -1
        return 0


###############################################################################
class Test_Bridge(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Bridge"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Bridge"].remove()
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)

    def test_costreduction(self):
        self.coin = 1
        self.assertEqual(self.plr.cardCost(self.g["Gold"]), 6)
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.cardCost(self.g["Gold"]), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

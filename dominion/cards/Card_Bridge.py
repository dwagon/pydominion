#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Bridge(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "+1 Buy +1 Coin. All cards (including cards in players hands) cost 1 less this turn, but not less than 0."
        self.name = "Bridge"
        self.buys = 1
        self.coin = 1
        self.cost = 4

    def hook_card_cost(self, game, player, card):
        """All cards (including cards in players' hands) cost 1
        less this turn, but not less than 0"""
        if self in player.piles[Piles.PLAYED]:
            return -1
        return 0


###############################################################################
class TestBridge(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bridge"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Bridge")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_cost_reduction(self):
        self.coin = 1
        self.assertEqual(self.plr.card_cost(self.g.get_card_from_pile("Gold")), 6)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.card_cost(self.g.get_card_from_pile("Gold")), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

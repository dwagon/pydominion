#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card
from dominion.Player import Piles


###############################################################################
class Card_Peddler(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 Card, +1 Action, +1 Coin. During your Buy phase, this
            costs 2 less per Action card you have in play, but not less than 0"""
        self.name = "Peddler"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 8

    def hook_this_card_cost(self, game, player):
        cost = 0
        for card in player.piles[Piles.PLAYED]:
            if card.isAction():
                cost -= 2
        return max(cost, -8)


###############################################################################
class Test_Peddler(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Peddler", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Peddler")

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_buy(self):
        self.plr.piles[Piles.PLAYED].set("Moat")
        cost = self.plr.card_cost(self.card)
        self.assertEqual(cost, 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

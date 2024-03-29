#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Merchantship(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "+2 coins; +2 coins next turn"
        self.name = "Merchant Ship"
        self.coin = 2
        self.cost = 5

    def duration(self, game, player):
        """Now and at the start of your next turn +2 coins"""
        player.output("2 more coins from Merchant Ship")
        player.coins.add(2)


###############################################################################
class Test_Merchantship(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Merchant Ship"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Merchant Ship")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a merchant ship"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
        self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Merchant Ship")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

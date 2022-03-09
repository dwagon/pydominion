#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Merchantship(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.SEASIDE
        self.desc = "+2 coins; +2 coins next turn"
        self.name = "Merchant Ship"
        self.coin = 2
        self.cost = 5

    def duration(self, game, player):
        """Now and at the start of your next turn +2 coins"""
        player.output("2 more coins from Merchant Ship")
        player.addCoin(2)


###############################################################################
class Test_Merchantship(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Merchant Ship"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Merchant Ship"].remove()
        self.plr.addCard(self.card, "hand")

    def test_playcard(self):
        """Play a merchant ship"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.durationpile.size(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.durationpile.size(), 0)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.played.size(), 1)
        self.assertEqual(self.plr.played[-1].name, "Merchant Ship")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

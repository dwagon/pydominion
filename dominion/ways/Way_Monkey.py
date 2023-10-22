#!/usr/bin/env python

import unittest
from dominion import Card, Game, Way, Piles


###############################################################################
class Way_Monkey(Way.Way):
    def __init__(self):
        Way.Way.__init__(self)
        self.base = Card.CardExpansion.MENAGERIE
        self.desc = "+1 Buy; +1 Coin"
        self.name = "Way of the Monkey"
        self.buys = 1
        self.coin = 1


###############################################################################
class TestMonkey(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            ways=["Way of the Monkey"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Moat")
        self.way = self.g.ways["Way of the Monkey"]

    def test_play(self):
        """Perform a Monkey"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.buys.get(), 1 + 1)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

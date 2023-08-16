#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Armory(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "Gain a card costing up to 4 putting it on top of your deck"
        self.name = "Armory"
        self.cost = 4

    def special(self, game, player):
        """Gain a card costing up to 4"""
        player.plr_gain_card(4, destination="deck")


###############################################################################
class Test_Armory(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Armory", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.armory = self.g["Armory"].remove()
        self.plr.add_card(self.armory, Piles.HAND)

    def test_gainzero(self):
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.armory)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())

    def test_gainone(self):
        self.plr.test_input = ["Moat"]
        self.plr.piles[Piles.DECK].empty()
        self.plr.play_card(self.armory)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertTrue(self.plr.piles[Piles.DISCARD].is_empty())
        self.assertLessEqual(self.plr.piles[Piles.DECK][-1].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

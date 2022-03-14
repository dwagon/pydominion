#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Armory(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = "Gain a card costing up to 4 putting it on top of your deck"
        self.name = "Armory"
        self.cost = 4

    def special(self, game, player):
        """Gain a card costing up to 4"""
        player.plrGainCard(4, destination="deck")


###############################################################################
class Test_Armory(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Armory", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.armory = self.g["Armory"].remove()
        self.plr.add_card(self.armory, "hand")

    def test_gainzero(self):
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.armory)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertTrue(self.plr.discardpile.is_empty())

    def test_gainone(self):
        self.plr.test_input = ["Moat"]
        self.plr.deck.empty()
        self.plr.play_card(self.armory)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertTrue(self.plr.discardpile.is_empty())
        self.assertLessEqual(self.plr.deck[-1].cost, 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

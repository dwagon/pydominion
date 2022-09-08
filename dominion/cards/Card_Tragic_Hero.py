#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Tragic_Hero(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.NOCTURNE
        self.desc = "+3 Cards; +1 Buys; If you have 8 or more cards in hand (after drawing), trash this and gain a Treasure."
        self.name = "Tragic Hero"
        self.cost = 5
        self.cards = 3
        self.buys = 1

    def special(self, game, player):
        if player.hand.size() >= 8:
            player.trash_card(self)
            player.plr_gain_card(cost=None, types={Card.TYPE_TREASURE: True})


###############################################################################
class Test_Tragic_Hero(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Tragic Hero"], badcards=["Fool's Gold"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Tragic Hero"].remove()

    def test_play(self):
        """Play a Tragic Hero with less than 8 cards"""
        self.plr.hand.set("Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.hand.size(), 1 + 3)

    def test_gainsomething(self):
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Get Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 3)
        self.assertIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

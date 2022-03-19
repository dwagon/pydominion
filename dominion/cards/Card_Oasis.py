#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Oasis(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = "+1 card, +1 action, +1 coin, discard 1 card"
        self.name = "Oasis"
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 3

    def special(self, game, player):
        """Discard a card"""
        player.plr_discard_cards()


###############################################################################
class Test_Oasis(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Oasis"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Oasis"].remove()
        self.plr.set_hand("Gold", "Copper", "Copper", "Copper", "Copper")
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play an oasis"""
        self.plr.test_input = ["discard gold", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_coins(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Page(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_TRAVELLER]
        self.base = Game.ADVENTURE
        self.desc = "+1 Card, +1 Action; Discard to replace with Treasure Hunter"
        self.name = "Page"
        self.traveller = True
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def hook_discard_this_card(self, game, player, source):
        """Replace with Treasure Hunter"""
        player.replace_traveller(self, "Treasure Hunter")


###############################################################################
class Test_Page(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Page"].remove()

    def test_page(self):
        """Play a page"""
        self.plr.set_hand()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.get_actions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

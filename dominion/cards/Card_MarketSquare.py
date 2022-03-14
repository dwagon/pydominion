#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_MarketSquare(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.DARKAGES
        self.desc = """+1 Card, +1 Action, +1 Buy.
        When one of your cards is trashed, you may discard this from your hand. If you do, gain a Gold."""
        self.name = "Market Square"
        self.cards = 1
        self.actions = 1
        self.buys = 1
        self.cost = 3

    def hook_trash_card(self, game, player, card):
        gold = player.plr_choose_options(
            "Discard Market Square to gain a Gold?",
            ("Keep Market Square in hand", False),
            ("Discard and gain a Gold", True),
        )
        if gold:
            player.discard_card(self)
            player.gain_card("Gold")


###############################################################################
class Test_MarketSquare(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Market Square"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Market Square"].remove()

    def test_play(self):
        """Play the card"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_trash_and_keep(self):
        """Choose to keep MS after a trash"""
        self.plr.set_hand("Copper", "Market Square")
        self.plr.test_input = ["keep"]
        self.plr.trash_card(self.plr.in_hand("Copper"))
        self.assertIsNotNone(self.plr.in_hand("Market Square"))

    def test_trash_and_discard(self):
        """Choose to keep MS after a trash"""
        self.plr.set_hand("Copper", "Market Square")
        self.plr.test_input = ["discard"]
        self.plr.trash_card(self.plr.in_hand("Copper"))
        self.assertIsNone(self.plr.in_hand("Market Square"))
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

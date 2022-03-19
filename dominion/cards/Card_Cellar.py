#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Cellar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = (
            "+1 Action; Discard any number of cards. +1 card per card discarded."
        )
        self.name = "Cellar"
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        todiscard = player.plr_discard_cards(
            0,
            anynum=True,
            prompt="Discard any number of cards and gain one per card discarded",
        )
        player.pickup_cards(len(todiscard))


###############################################################################
class Test_Cellar(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cellar"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g["Cellar"].remove()

    def test_none(self):
        self.plr.set_hand("Estate", "Copper", "Silver")
        self.plr.add_card(self.ccard, "hand")
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.hand.size(), 3)

    def test_one(self):
        self.plr.set_hand("Estate", "Copper", "Silver")
        self.plr.set_deck("Province", "Gold")
        self.plr.add_card(self.ccard, "hand")
        self.plr.test_input = ["discard estate", "finish"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.deck[-1].name, "Province")
        self.assertIsNotNone(self.plr.in_hand("Gold"))
        self.assertEqual(self.plr.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

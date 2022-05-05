#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Baron(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "+1 Buy. You may discard an Estate card. If you do +4 Coin. Otherwise, gain an Estate card."
        self.name = "Baron"
        self.cost = 4
        self.buys = 1

    def special(self, game, player):
        """You may discard an Estate card. If you do +4 Coin. Otherwise,
        gain an estate card"""
        hasEstate = player.hand["Estate"]
        if hasEstate:
            ans = player.plr_choose_options(
                "Discard Estate?",
                ("Keep Estate - Gain another", False),
                ("Discard an Estate - Gain +4 Coin", True),
            )
            if ans:
                player.discard_card(hasEstate)
                player.add_coins(4)
                return
        player.gain_card("Estate")


###############################################################################
class Test_Baron(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Baron"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.baron = self.g["Baron"].remove()

    def test_play(self):
        self.plr.add_card(self.baron, "hand")
        self.plr.test_input = ["Keep"]
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_noestate(self):
        self.plr.hand.set("Copper", "Copper", "Copper")
        self.plr.add_card(self.baron, "hand")
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.discardpile[0].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 1)

    def test_discardestate(self):
        self.plr.hand.set("Gold", "Estate", "Copper")
        self.plr.add_card(self.baron, "hand")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_coins(), 4)
        self.assertEqual(self.plr.discardpile[0].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertNotIn("Estate", self.plr.hand)

    def test_keepestate(self):
        self.plr.hand.set("Estate", "Gold", "Copper")
        self.plr.add_card(self.baron, "hand")
        self.plr.test_input = ["Keep"]
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.discardpile[0].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIn("Estate", self.plr.in_hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

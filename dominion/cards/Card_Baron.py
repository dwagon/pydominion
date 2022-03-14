#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


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
        hasEstate = player.in_hand("Estate")
        if hasEstate:
            ans = player.plrChooseOptions(
                "Discard Estate?",
                ("Keep Estate - Gain another", False),
                ("Discard an Estate - Gain +4 Gold", True),
            )
            if ans:
                player.discard_card(hasEstate)
                player.addCoin(4)
                return
        player.output("Gained an Estate")
        player.gain_card("Estate")


###############################################################################
class Test_Baron(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Baron"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.baron = self.g["Baron"].remove()

    def test_play(self):
        self.plr.add_card(self.baron, "hand")
        self.plr.test_input = ["Keep"]
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_noestate(self):
        self.plr.set_hand("Copper", "Copper", "Copper")
        self.plr.add_card(self.baron, "hand")
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.discardpile[0].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 1)

    def test_discardestate(self):
        self.plr.set_hand("Gold", "Estate", "Copper")
        self.plr.add_card(self.baron, "hand")
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_coins(), 4)
        self.assertEqual(self.plr.discardpile[0].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertEqual(self.plr.in_hand("Estate"), None)

    def test_keepestate(self):
        self.plr.set_hand("Estate", "Gold", "Copper")
        self.plr.add_card(self.baron, "hand")
        self.plr.test_input = ["Keep"]
        self.plr.play_card(self.baron)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.discardpile[0].name, "Estate")
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertNotEqual(self.plr.in_hand("Estate"), None)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

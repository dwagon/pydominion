#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game


###############################################################################
class Boon_Skys_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.TYPE_BOON
        self.base = Game.NOCTURNE
        self.desc = "You may discard 3 cards to gain a Gold."
        self.name = "The Sky's Gift"
        self.purchasable = False

    def special(self, game, player):
        dc = player.plr_discard_cards(anynum=True, prompt="Discard 3 cards to gain a Gold")
        if len(dc) >= 3:
            player.gain_card("Gold")
            player.output("Gained a Gold")


###############################################################################
class Test_Skys_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Sky's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g["Bard"].remove()

    def test_skys_gift(self):
        """Discard 3 cards to gain a gold"""
        self.plr.hand.set("Copper", "Estate", "Duchy", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Copper", "Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertIsNotNone(self.plr.discardpile["Gold"])

    def test_skys_no_gift(self):
        """Discard less than three cards to gain nothing"""
        self.plr.hand.set("Copper", "Estate", "Duchy", "Silver")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Copper", "Estate", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertNotIn("Gold", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

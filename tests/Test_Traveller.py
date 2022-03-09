#!/usr/bin/env python

import unittest
from dominion import Game


###############################################################################
class Test_load_travellers(unittest.TestCase):
    def test_needtravellers(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.assertTrue(self.g.loaded_travellers)


###############################################################################
class Test_replace_traveller(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Page"].remove()
        self.plr.addCard(self.card, "hand")

    def test_replace(self):
        """Replace a traveller"""
        self.plr.test_input = ["replace"]
        self.plr.playCard(self.card)
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIsNone(self.plr.in_hand("Page"))
        self.assertIsNotNone(self.plr.in_hand("Treasure Hunter"))

    def test_dont_replace(self):
        """Choose not to replace a traveller"""
        self.plr.test_input = ["keep"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIsNotNone(self.plr.in_hand("Page"))
        self.assertIsNone(self.plr.in_hand("Treasure Hunter"))

    def test_replacement_not_available(self):
        """Try and replace a traveller when the replacement isn't available"""
        self.plr.test_input = ["replace"]
        # TODO

    def test_not_played(self):
        """Try and replace a traveller when it hasn't been played"""
        self.plr.test_input = ["replace"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIsNotNone(self.plr.in_hand("Page"))
        self.assertIsNone(self.plr.in_hand("Treasure Hunter"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

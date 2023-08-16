#!/usr/bin/env python

import unittest
from dominion import Game, Piles


###############################################################################
class Test_load_travellers(unittest.TestCase):
    def test_needtravellers(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.assertTrue(self.g.loaded_travellers)


###############################################################################
class Test_replace_traveller(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Page"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_replace(self):
        """Replace a traveller"""
        self.plr.test_input = ["replace"]
        self.plr.play_card(self.card)
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertNotIn("Page", self.plr.piles[Piles.HAND])
        self.assertIn("Treasure Hunter", self.plr.piles[Piles.HAND])

    def test_dont_replace(self):
        """Choose not to replace a traveller"""
        self.plr.test_input = ["keep"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIn("Page", self.plr.piles[Piles.HAND])
        self.assertNotIn("Treasure Hunter", self.plr.piles[Piles.HAND])

    def test_replacement_not_available(self):
        """Try and replace a traveller when the replacement isn't available"""
        self.plr.test_input = ["replace"]
        # TODO

    def test_not_played(self):
        """Try and replace a traveller when it hasn't been played"""
        self.plr.test_input = ["replace"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIn("Page", self.plr.piles[Piles.HAND])
        self.assertNotIn("Treasure Hunter", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

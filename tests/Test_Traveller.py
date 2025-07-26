#!/usr/bin/env python

import unittest

from dominion import Game, Piles
from dominion.Game import Flags


###############################################################################
class TestLoadTravellers(unittest.TestCase):
    def test_need_travellers(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.assertTrue(self.g.flags[Flags.LOADED_TRAVELLERS])


###############################################################################
class TestReplaceTraveller(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Page"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Page")

    def test_replace(self) -> None:
        """Replace a traveller"""
        self.plr.add_card(self.card, Piles.PLAYED)
        self.plr.test_input = ["replace"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertNotIn("Page", self.plr.piles[Piles.HAND])
        self.assertIn("Treasure Hunter", self.plr.piles[Piles.HAND])

    def test_dont_replace(self) -> None:
        """Choose not to replace a traveller"""
        self.plr.add_card(self.card, Piles.PLAYED)
        self.plr.test_input = ["keep"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIn("Page", self.plr.piles[Piles.PLAYED])
        self.assertNotIn("Treasure Hunter", self.plr.piles[Piles.HAND])

    def test_replacement_not_available(self) -> None:
        """Try and replace a traveller when the replacement isn't available"""
        self.plr.test_input = ["replace"]
        # TODO

    def test_not_played(self) -> None:
        """Try and replace a traveller when it hasn't been played"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["replace"]
        self.plr.replace_traveller(self.card, "Treasure Hunter")
        self.assertIn("Page", self.plr.piles[Piles.HAND])
        self.assertNotIn("Treasure Hunter", self.plr.piles[Piles.HAND])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

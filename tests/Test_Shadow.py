#!/usr/bin/env python

import unittest

from dominion import Game, Piles


###############################################################################
class TestShadow(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Alley"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    ###########################################################################
    def test_shuffle(self) -> None:
        """Ensure the shadows are shuffled to the bottom"""
        self.plr.piles[Piles.DECK].set("Copper", "Duchy")
        self.plr.piles[Piles.DISCARD].set("Silver", "Alley", "Estate")
        self.plr.refill_deck()
        self.assertTrue(self.plr.piles[Piles.DECK][0].isShadow())
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

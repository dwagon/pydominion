#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Worm(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Exile an Estate from the Supply."
        self.name = "Way of the Worm"

    def special(self, game, player):
        player.exile_card("Estate")


###############################################################################
class Test_Worm(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            waycards=["Way of the Worm"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Worm"]

    def test_play(self):
        """Perform a Worm"""
        self.plr.addCard(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.assertIsNotNone(self.plr.in_exile("Estate"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

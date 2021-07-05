#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Monkey(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "+1 Buy; +1 Coin"
        self.name = "Way of the Monkey"
        self.buys = 1
        self.coin = 1


###############################################################################
class Test_Monkey(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            waycards=["Way of the Monkey"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Monkey"]

    def test_play(self):
        """Perform a Monkey"""
        self.plr.addCard(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

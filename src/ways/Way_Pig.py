#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Pig(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "+1 Card; +1 Action"
        self.name = "Way of the Pig"
        self.cards = 1
        self.actions = 1


###############################################################################
class Test_Pig(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=1,
            waycards=["Way of the Pig"],
            initcards=["Moat"],
            badcards=["Duchess"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Moat"].remove()
        self.way = self.g.ways["Way of the Pig"]

    def test_play(self):
        """Perform a Pig"""
        self.plr.addCard(self.card, "hand")
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

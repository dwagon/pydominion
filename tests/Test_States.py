#!/usr/bin/env python

import unittest
from dominion import Game


###############################################################################
class Test_assignState(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True,
            numplayers=2,
            initcards=["StateTester"],
            statepath="tests/states",
            cardpath="tests/cards",
            numstacks=1,
            boonpath="tests/boons",
        )
        self.g.start_game()
        self.plr, self.other = self.g.player_list()

    def test_non_unique(self):
        self.plr.assign_state("NonUnique")
        st = self.plr.states[0]
        self.assertEqual(st.name, "NonUnique")

    def test_unique(self):
        self.plr.assign_state("Unique")
        self.assertTrue(self.plr.has_state("Unique"))
        self.assertFalse(self.other.has_state("Unique"))
        self.other.assign_state("Unique")
        self.assertFalse(self.plr.has_state("Unique"))
        self.assertTrue(self.other.has_state("Unique"))

    def test_has_state(self):
        self.plr.assign_state("NonUnique")
        self.assertTrue(self.plr.has_state("NonUnique"))
        self.assertFalse(self.plr.has_state("Bunny"))

    def test_remove_state(self):
        self.plr.assign_state("NonUnique")
        self.assertTrue(self.plr.has_state("NonUnique"))
        self.plr.remove_state("NonUnique")
        self.assertFalse(self.plr.has_state("NonUnique"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

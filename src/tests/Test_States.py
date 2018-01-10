#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_assignState(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Fool'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()

    def test_non_unique(self):
        self.plr.assign_state('Deluded')
        st = self.plr.states[0]
        self.assertEqual(st.name, 'Deluded')

    def test_unique(self):
        self.plr.assign_state('Lost in the Woods')
        self.assertTrue(self.plr.has_state('Lost in the Woods'))
        self.assertFalse(self.other.has_state('Lost in the Woods'))
        self.other.assign_state('Lost in the Woods')
        self.assertFalse(self.plr.has_state('Lost in the Woods'))
        self.assertTrue(self.other.has_state('Lost in the Woods'))

    def test_has_state(self):
        self.plr.assign_state('Deluded')
        self.assertTrue(self.plr.has_state('Deluded'))
        self.assertFalse(self.plr.has_state('Bunny'))

    def test_remove_state(self):
        self.plr.assign_state('Deluded')
        self.assertTrue(self.plr.has_state('Deluded'))
        self.plr.remove_state('Deluded')
        self.assertFalse(self.plr.has_state('Deluded'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

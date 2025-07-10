#!/usr/bin/env python

import unittest

from dominion import Game


###############################################################################
class TestArtifact(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2)
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_assign_artifact(self):
        self.plr.assign_artifact("Flag")
        self.assertEqual(self.plr.artifacts[0].name, "Flag")

    def test_assign_artifact_twice(self):
        self.plr.assign_artifact("Flag")
        self.assertEqual(len(self.plr.artifacts), 1)
        self.plr.assign_artifact("Flag")
        self.assertEqual(len(self.plr.artifacts), 1)

    def test_reassign_artifact(self):
        self.plr.assign_artifact("Flag")
        self.vic.assign_artifact("Flag")
        self.assertEqual(len(self.plr.artifacts), 0)
        self.assertEqual(len(self.vic.artifacts), 1)

    def test_remove_artifact(self):
        self.plr.assign_artifact("Flag")
        self.plr.remove_artifact("Flag")
        self.assertEqual(len(self.plr.artifacts), 0)

    def test_has_artifact(self):
        self.plr.assign_artifact("Flag")
        self.assertTrue(self.plr.has_artifact("Flag"))
        self.assertFalse(self.plr.has_artifact("Key"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

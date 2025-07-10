#!/usr/bin/env python
""" Test the run_game module """

import unittest

from dominion import Game, rungame


###############################################################################
class Test_parse_args(unittest.TestCase):
    """Test argument parsing"""

    def test_defaults(self):
        """Test that no args gives us the defaults"""
        args = rungame.parse_cli_args([])
        self.assertEqual(args.numplayers, 2)
        self.assertEqual(args.prosperity, False)
        self.assertEqual(args.initcards, [])

    def test_prosperity(self):
        """Test Prosperity flag"""
        args = rungame.parse_cli_args(["--prosperity"])
        self.assertEqual(args.prosperity, True)

    def test_numplayers(self):
        """Test changing number of players"""
        args = rungame.parse_cli_args(["--numplayers", "4"])
        self.assertEqual(args.numplayers, 4)

    def test_events(self):
        """Test using events"""
        args = rungame.parse_cli_args(["--events", "Alms"])
        self.assertEqual(args.events, ["Alms"])
        g = Game.TestGame(**vars(args))
        g.start_game()
        self.assertIn("Alms", g.events)

    def test_use_card(self):
        """Test specifying a card"""
        args = rungame.parse_cli_args(["--card", "Moat"])
        g = Game.TestGame(**vars(args))
        g.start_game()
        self.assertIn("Moat", g.card_piles)

    def test_use_landmark(self):
        """Test specifying a landmark"""
        args = rungame.parse_cli_args(["--landmark", "Aqueduct"])
        g = Game.TestGame(**vars(args))
        g.start_game()
        self.assertIn("Aqueduct", g.landmarks)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

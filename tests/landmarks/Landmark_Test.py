#!/usr/bin/env python
"""Test Landmark"""
import unittest

from dominion import Card, Landmark


###############################################################################
class Landmark_Test(Landmark.Landmark):
    """Test"""

    def __init__(self) -> None:
        Landmark.Landmark.__init__(self)
        self.base = Card.CardExpansion.TEST
        self.name = "Test"


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

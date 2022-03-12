#!/usr/bin/env python

import unittest
from dominion import PlayArea
from dominion import Card


###############################################################################
class CardTester(object):
    def __init__(self, name):
        self.name = name


###############################################################################
class Test_PlayArea(unittest.TestCase):
    def test_count(self):
        """Test count"""
        CT = CardTester
        s = PlayArea.PlayArea([CT("a"), CT("b"), CT("c"), CT("c")])
        self.assertEqual(s.count("a"), 1)
        self.assertEqual(s.count(CT("c")), 2)

    def test_add(self):
        card_a = Card.Card()
        card_b = Card.Card()
        s = PlayArea.PlayArea([card_a])
        s.add(card_b)
        self.assertEqual(s.cards, [card_a, card_b])

    def test_remove(self):
        s = PlayArea.PlayArea(["a", "b"])
        s.remove("b")
        self.assertEqual(s.cards, ["a"])

    def test_len(self):
        s = PlayArea.PlayArea(["a", "b"])
        self.assertEqual(len(s), 2)

    def test_eq(self):
        s = PlayArea.PlayArea(["a", "b"])
        t = PlayArea.PlayArea(["a", "b"])
        self.assertEqual(s, t)
        self.assertEqual(s, ["a", "b"])
        self.assertNotEqual(s, ["a"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
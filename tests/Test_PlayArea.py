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
        s = PlayArea.PlayArea("name", "game", [CT("a"), CT("b"), CT("c"), CT("c")])
        self.assertEqual(s.count("a"), 1)
        self.assertEqual(s.count(CT("c")), 2)

    def test_add(self):
        card_a = Card.Card()
        card_b = Card.Card()
        s = PlayArea.PlayArea("name", "game", [card_a])
        s.add(card_b)
        self.assertEqual(s._cards, [card_a, card_b])

    def test_remove(self):
        s = PlayArea.PlayArea("name", "game", ["a", "b"])
        s.remove("b")
        self.assertEqual(s._cards, ["a"])

    def test_len(self):
        s = PlayArea.PlayArea("name", "game", ["a", "b"])
        self.assertEqual(len(s), 2)

    def test_eq(self):
        s = PlayArea.PlayArea("name", "game", ["a", "b"])
        t = PlayArea.PlayArea("name", "game", ["a", "b"])
        self.assertEqual(s, t)
        self.assertEqual(s, ["a", "b"])
        self.assertNotEqual(s, ["a"])

    def test_top_card(self):
        """ Test the top_card() method"""
        s = PlayArea.PlayArea("name", "game", ["a", "b", "c"])
        s.addToTop("z")
        self.assertEqual(s.top_card(), "z")
        nxt = s.next_card()
        self.assertEqual(nxt, "z")

    def test_iter(self):
        """ Test the iterator """
        bits = ["a", "b", "c", "d"]
        s = PlayArea.PlayArea("name", "game", bits)
        found = set()
        for obj in s:
            found.add(obj)
        self.assertEqual(len(found), 4)
        self.assertEqual(found, set(bits))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

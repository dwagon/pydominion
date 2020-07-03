#!/usr/bin/env python

import unittest
from PlayArea import PlayArea


###############################################################################
class CardTester(object):
    def __init__(self, name):
        self.name = name


###############################################################################
class Test_PlayArea(unittest.TestCase):
    def test_count(self):
        """ Test count """
        CT = CardTester
        s = PlayArea([CT('a'), CT('b'), CT('c'), CT('c')])
        self.assertEqual(s.count('a'), 1)
        self.assertEqual(s.count(CT('c')), 2)

    def test_add(self):
        s = PlayArea(['a'])
        s.add('b')
        self.assertEqual(s.cards, ['a', 'b'])

    def test_remove(self):
        s = PlayArea(['a', 'b'])
        s.remove('b')
        self.assertEqual(s.cards, ['a'])

    def test_len(self):
        s = PlayArea(['a', 'b'])
        self.assertEqual(len(s), 2)

    def test_eq(self):
        s = PlayArea(['a', 'b'])
        t = PlayArea(['a', 'b'])
        self.assertEqual(s, t)
        self.assertEqual(s, ['a', 'b'])
        self.assertNotEqual(s, ['a'])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
""" Test that Counter class works """
# pylint: disable=protected-access

import unittest

from dominion.Counter import Counter


###############################################################################
class Test_Counter(unittest.TestCase):
    """Test Counter"""

    def test_set(self) -> None:
        """Test set()"""
        cntr = Counter("Foo", 3)
        cntr.set(5)
        self.assertEqual(cntr._value, 5)

    def test_get(self) -> None:
        """Test get()"""
        cntr = Counter("Foo", 3)
        self.assertEqual(cntr.get(), 3)

    def test_add(self) -> None:
        """Test add()"""
        cntr = Counter("Foo", 3)
        cntr.add(5)
        self.assertEqual(cntr.get(), 8)

    def test_add_dunder(self) -> None:
        """Test __add__()"""
        cntr = Counter("Foo", 3)
        cntr += 5
        self.assertEqual(cntr.get(), 8)
        cntr += Counter("Bar", 1)
        self.assertEqual(cntr.get(), 9)

    def test_sub_dunder(self) -> None:
        """Test __sub__()"""
        cntr = Counter("Foo", 5)
        cntr -= 2
        self.assertEqual(cntr.get(), 3)
        cntr -= Counter("Bar", 1)
        self.assertEqual(cntr.get(), 2)

    def test_bool(self) -> None:
        """Test __bool__"""
        self.assertTrue(Counter("Foo", 1))
        self.assertFalse(Counter("Foo", 0))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

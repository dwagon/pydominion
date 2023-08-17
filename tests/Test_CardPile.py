#!/usr/bin/env python

import unittest

from dominion import Game, CardPile


###############################################################################
class FakeCard:
    def __init__(self, name="Fake Card"):
        self.name = name

    def __str__(self):
        return f"<{self.name}>"


###############################################################################
class TestCardPile(unittest.TestCase):
    def setUp(self):
        mock_card = FakeCard
        g = Game.Game()
        self.cp = CardPile.CardPile(
            cardname="test_card", klass=mock_card, game=g, pile_size=5
        )

    def test_remove(self):
        """Test the remove() function"""
        self.assertEqual(len(self.cp), 5)
        card = self.cp.remove()
        self.assertEqual(len(self.cp), 4)
        self.assertTrue(isinstance(card, FakeCard))

    def test_remove_empty(self):
        """Test removing from an empty pile"""
        while True:
            card = self.cp.remove()
            if card is None:
                break
        card = self.cp.remove()
        self.assertIsNone(card)

    def test_add(self):
        self.assertEqual(len(self.cp), 5)
        self.cp.add(FakeCard())
        self.assertEqual(len(self.cp), 6)

    def test_empty(self):
        self.assertFalse(self.cp.is_empty())
        self.assertTrue(self.cp)
        count = 0
        while True:
            card = self.cp.remove()
            if card is None:
                break
            count += 1
        self.assertEqual(count, 5)
        self.assertIsNone(self.cp.remove())
        self.assertTrue(self.cp.is_empty())
        self.assertFalse(self.cp)

    def test_rotate(self):
        """Test rotating a card pile"""
        while True:
            card = self.cp.remove()
            if card is None:
                break
        self.cp.add(FakeCard(name="Foo"))
        self.cp.add(FakeCard(name="Bar"))
        self.cp.add(FakeCard(name="Baz"))
        self.cp.rotate()
        self.assertEqual(self.cp.top_card(), "Bar")

    def test_rotate_empty(self):
        """Test rotating an empty card pile"""
        while True:
            card = self.cp.remove()
            if card is None:
                break
        self.cp.rotate()
        self.assertIsNone(self.cp.top_card())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

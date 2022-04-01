#!/usr/bin/env python

import unittest

from dominion import Game, CardPile


###############################################################################
class Fake_Card:
    def __init__(self):
        self.name = "Fake Card"


###############################################################################
class Test_CardPile(unittest.TestCase):
    def setUp(self):
        mock_card = Fake_Card
        g = Game.Game()
        self.cp = CardPile.CardPile(cardname="test_card", klass=mock_card, game=g, pile_size=5)

    def test_remove(self):
        self.assertEqual(len(self.cp), 5)
        card = self.cp.remove()
        self.assertEqual(len(self.cp), 4)
        self.assertTrue(isinstance(card, Fake_Card))

    def test_add(self):
        self.assertEqual(len(self.cp), 5)
        self.cp.add(Fake_Card())
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


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

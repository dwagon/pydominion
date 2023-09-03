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
        game = Game.Game()
        self.card_pile = CardPile.CardPile(game)
        self.card_pile.init_cards(num_cards=5, card_class=mock_card)

    def test_remove(self):
        """Test the remove() function"""
        self.assertEqual(len(self.card_pile), 5)
        card = self.card_pile.remove()
        self.assertEqual(len(self.card_pile), 4)
        self.assertTrue(isinstance(card, FakeCard))

    def test_remove_named(self):
        """Test the remove() function naming a specific card"""
        index = 0
        for card in self.card_pile:
            card.name = f"Fake_{index}"
            index += 1
        card = self.card_pile.remove("Fake_2")
        self.assertEqual(card.name, "Fake_2")
        for card in self.card_pile:
            self.assertNotEqual(card.name, "Fake_2")

    def test_remove_empty(self):
        """Test removing from an empty pile"""
        while True:
            card = self.card_pile.remove()
            if card is None:
                break
        card = self.card_pile.remove()
        self.assertIsNone(card)

    def test_add(self):
        self.assertEqual(len(self.card_pile), 5)
        self.card_pile.add(FakeCard())
        self.assertEqual(len(self.card_pile), 6)

    def test_empty(self):
        self.assertFalse(self.card_pile.is_empty())
        self.assertTrue(self.card_pile)
        count = 0
        while True:
            card = self.card_pile.remove()
            if card is None:
                break
            count += 1
        self.assertEqual(count, 5)
        self.assertIsNone(self.card_pile.remove())
        self.assertTrue(self.card_pile.is_empty())
        self.assertFalse(self.card_pile)

    def test_rotate(self):
        """Test rotating a card pile"""
        while True:
            card = self.card_pile.remove()
            if card is None:
                break
        self.card_pile.add(FakeCard(name="Foo"))
        self.card_pile.add(FakeCard(name="Bar"))
        self.card_pile.add(FakeCard(name="Baz"))
        self.card_pile.rotate()
        self.assertEqual(self.card_pile.top_card(), "Bar")

    def test_rotate_empty(self):
        """Test rotating an empty card pile"""
        while True:
            card = self.card_pile.remove()
            if card is None:
                break
        self.card_pile.rotate()
        self.assertIsNone(self.card_pile.top_card())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

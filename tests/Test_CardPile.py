#!/usr/bin/env python

import unittest

from dominion import Game, CardPile, Card, NoCardException


###############################################################################
class FakeCard(Card.Card):
    def __init__(self, name: str = "Fake Card") -> None:
        self.name = name

    def __str__(self) -> str:
        return f"<{self.name}>"


###############################################################################
class TestCardPile(unittest.TestCase):
    def setUp(self) -> None:
        mock_card = FakeCard
        self.game = Game.Game()
        self.card_pile = CardPile.CardPile(self.game)
        self.card_pile.init_cards(num_cards=5, card_class=mock_card)

    def test_remove(self) -> None:
        """Test the remove() function"""
        self.assertEqual(len(self.card_pile), 5)
        card = self.card_pile.remove()
        self.assertEqual(len(self.card_pile), 4)
        self.assertTrue(isinstance(card, FakeCard))

    def test_remove_named(self) -> None:
        """Test the remove() function naming a specific card"""
        index = 0
        for card in self.card_pile:
            card.name = f"Fake_{index}"
            index += 1
        card = self.card_pile.remove("Fake_2")
        self.assertEqual(card.name, "Fake_2")
        for card in self.card_pile:
            self.assertNotEqual(card.name, "Fake_2")

    def test_remove_empty(self) -> None:
        """Test removing from an empty pile"""
        empty_card_pile = CardPile.CardPile(self.game)
        with self.assertRaises(NoCardException):
            card = empty_card_pile.remove()

    def test_add(self) -> None:
        self.assertEqual(len(self.card_pile), 5)
        self.card_pile.add(FakeCard())
        self.assertEqual(len(self.card_pile), 6)

    def test_empty(self) -> None:
        self.assertFalse(self.card_pile.is_empty())
        self.assertTrue(self.card_pile)
        count = 0
        while True:
            try:
                card = self.card_pile.remove()
            except NoCardException:
                break
            count += 1
        self.assertEqual(count, 5)
        with self.assertRaises(NoCardException):
            self.card_pile.remove()
        self.assertTrue(self.card_pile.is_empty())
        self.assertFalse(self.card_pile)

    def test_rotate(self) -> None:
        """Test rotating a card pile"""
        card_pile = CardPile.CardPile(self.game)

        card_pile.add(FakeCard(name="Foo"))
        card_pile.add(FakeCard(name="Bar"))
        card_pile.add(FakeCard(name="Baz"))
        card_pile.rotate()
        self.assertEqual(card_pile.top_card(), "Bar")

    def test_rotate_empty(self) -> None:
        """Test rotating an empty card pile"""
        card_pile = CardPile.CardPile(self.game)

        card_pile.rotate()
        with self.assertRaises(NoCardException):
            card_pile.top_card()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

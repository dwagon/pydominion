#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Patrician
https://wiki.dominionstrategy.com/index.php/Emporium"""
import unittest
from dominion import Card, Game, CardPile, game_setup, Keys


###############################################################################
class Card_PatricianSplit(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Patrician"
        self.base = Card.CardExpansion.EMPIRES

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = PatricianCardPile(game)
        return card_pile


###############################################################################
class PatricianCardPile(CardPile.CardPile):
    def __init__(self, game):
        mapping = game_setup.get_card_classes("Split", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Split_Patrician import Card_Patrician
        from dominion.cards.Split_Emporium import Card_Emporium

        for card_class in (Card_Patrician, Card_Emporium):
            for _ in range(5):
                self.cards.insert(0, card_class())


###############################################################################
class TestEncampmentPile(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Patrician"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_pile(self):
        self.assertEqual(len(self.g.card_piles["Patrician"]), 10)
        card = self.g.get_card_from_pile("Patrician")
        self.assertEqual(card.name, "Patrician")
        self.assertEqual(len(self.g.card_piles["Patrician"]), 9)
        for _ in range(5):
            card = self.g.get_card_from_pile("Patrician")
        self.assertEqual(card.name, "Emporium")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Catapult
https://wiki.dominionstrategy.com/index.php/Rocks"""
import unittest
from dominion import Card, Game, CardPile, game_setup, Keys


###############################################################################
class Card_CatapultSplit(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Catapult"
        self.base = Card.CardExpansion.EMPIRES

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = CatapultCardPile(game)
        return card_pile


###############################################################################
class CatapultCardPile(CardPile.CardPile):
    def __init__(self, game):
        mapping = game_setup.get_card_classes("Split", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Split_Catapult import Card_Catapult
        from dominion.cards.Split_Rocks import Card_Rocks

        for card_class in (Card_Catapult, Card_Rocks):
            for _ in range(5):
                self.cards.insert(0, card_class())


###############################################################################
class TestEncampmentPile(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Catapult"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_pile(self):
        self.assertEqual(len(self.g.card_piles["Catapult"]), 10)
        card = self.g.get_card_from_pile("Catapult")
        self.assertEqual(card.name, "Catapult")
        self.assertEqual(len(self.g.card_piles["Catapult"]), 9)
        for _ in range(5):
            card = self.g.get_card_from_pile("Catapult")
        self.assertEqual(card.name, "Rocks")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

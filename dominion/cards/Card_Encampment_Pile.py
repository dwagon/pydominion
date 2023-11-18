#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Encampment
    https://wiki.dominionstrategy.com/index.php/Plunder"""
import unittest
from dominion import Card, Game, CardPile


###############################################################################
class Card_EncampmentSplit(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Encampment"
        self.base = Card.CardExpansion.EMPIRES

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = EncampmentCardPile(game)
        return card_pile


###############################################################################
class EncampmentCardPile(CardPile.CardPile):
    def __init__(self, game):
        mapping = game.get_card_classes("Split", game.paths["cards"], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Split_Encampment import Card_Encampment
        from dominion.cards.Split_Plunder import Card_Plunder

        for card_class in (Card_Encampment, Card_Plunder):
            for _ in range(5):
                self.cards.insert(0, card_class())


###############################################################################
class TestEncampmentPile(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Encampment"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_pile(self):
        self.assertEqual(len(self.g.card_piles["Encampment"]), 10)
        card = self.g.get_card_from_pile("Encampment")
        self.assertEqual(card.name, "Encampment")
        self.assertEqual(len(self.g.card_piles["Encampment"]), 9)
        for _ in range(5):
            card = self.g.get_card_from_pile("Encampment")
        self.assertEqual(card.name, "Plunder")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

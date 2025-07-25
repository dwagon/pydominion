#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Settlers
https://wiki.dominionstrategy.com/index.php/Bustling_Village"""
import unittest
from dominion import Card, Game, CardPile, game_setup


###############################################################################
class Card_PatricianSplit(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.name = "Settlers"
        self.base = Card.CardExpansion.EMPIRES

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = SettlersCardPile(game)
        return card_pile


###############################################################################
class SettlersCardPile(CardPile.CardPile):
    def __init__(self, game) -> None:
        mapping = game_setup.get_card_classes("Split", game.paths["cards"], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards: int = 0, card_class=None) -> None:
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Split_Settlers import Card_Settlers
        from dominion.cards.Split_Bustling_Village import Card_BustlingVillage

        for card_class in (Card_Settlers, Card_BustlingVillage):
            for _ in range(5):
                self.cards.insert(0, card_class())


###############################################################################
class TestEncampmentPile(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Settlers"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_pile(self) -> None:
        self.assertEqual(len(self.g.card_piles["Settlers"]), 10)
        card = self.g.get_card_from_pile("Settlers")
        self.assertEqual(card.name, "Settlers")
        self.assertEqual(len(self.g.card_piles["Settlers"]), 9)
        for _ in range(5):
            card = self.g.get_card_from_pile("Settlers")
        self.assertEqual(card.name, "Bustling Village")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

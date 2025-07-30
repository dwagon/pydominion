#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Gladiator
https://wiki.dominionstrategy.com/index.php/Fortune"""
import unittest
from dominion import Card, Game, CardPile, Keys, game_setup


###############################################################################
class Card_GladiatorSplit(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.name = "Gladiator"
        self.base = Card.CardExpansion.EMPIRES

    @classmethod
    def cardpile_setup(cls, game: Game.Game) -> CardPile.CardPile:
        return GladiatorCardPile(game)


###############################################################################
class GladiatorCardPile(CardPile.CardPile):
    def __init__(self, game: Game.Game) -> None:
        mapping = game_setup.get_card_classes("Split", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards: int = 0, card_class: type[Card.Card] | None = None) -> None:
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Split_Gladiator import Card_Gladiator
        from dominion.cards.Split_Fortune import Card_Fortune

        for card_class in (Card_Gladiator, Card_Fortune):
            for _ in range(5):
                self.cards.insert(0, card_class())


###############################################################################
class TestGladiatorPile(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Gladiator"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_pile(self) -> None:
        self.assertEqual(len(self.g.card_piles["Gladiator"]), 10)
        card = self.g.get_card_from_pile("Gladiator")
        self.assertEqual(card.name, "Gladiator")
        self.assertEqual(len(self.g.card_piles["Gladiator"]), 9)
        for _ in range(5):
            card = self.g.get_card_from_pile("Gladiator")
        self.assertEqual(card.name, "Fortune")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

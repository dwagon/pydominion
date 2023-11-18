#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Sauna
    https://wiki.dominionstrategy.com/index.php/Avanto"""
import unittest
from dominion import Card, Game, CardPile, Keys


###############################################################################
class Card_SaunaSplit(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.name = "Sauna"
        self.base = Card.CardExpansion.PROMO

    @classmethod
    def cardpile_setup(cls, game: Game.Game) -> CardPile.CardPile:
        return SaunaCardPile(game)


###############################################################################
class SaunaCardPile(CardPile.CardPile):
    def __init__(self, game: Game.Game) -> None:
        mapping = game.get_card_classes("Split", game.paths[Keys.CARDS], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(
        self, num_cards: int = 0, card_class: type[Card.Card] | None = None
    ) -> None:
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Split_Sauna import Card_Sauna
        from dominion.cards.Split_Avanto import Card_Avanto

        for card_class in (Card_Sauna, Card_Avanto):
            for _ in range(5):
                self.cards.insert(0, card_class())


###############################################################################
class TestSaunaPile(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Sauna"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_pile(self) -> None:
        self.assertEqual(len(self.g.card_piles["Sauna"]), 10)
        card = self.g.get_card_from_pile("Sauna")
        self.assertEqual(card.name, "Sauna")
        self.assertEqual(len(self.g.card_piles["Sauna"]), 9)
        for _ in range(5):
            card = self.g.get_card_from_pile("Sauna")
        self.assertEqual(card.name, "Avanto")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

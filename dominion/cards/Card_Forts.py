#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fort"""

import unittest
from dominion import Card, Game, Piles, CardPile


###############################################################################
class Card_Forts(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Forts"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = Card.CardType.ACTION

    def setup(self, game):
        game.cardpiles["Forts"] = FortCardPile(game)


###############################################################################
class FortCardPile(CardPile.CardPile):
    def __init__(self, game, pile_size=10):
        self.mapping = game.get_card_classes("Fort", game.paths["cards"], "Card_")
        super().__init__(cardname="Forts", klass=None, game=game, pile_size=pile_size)

    def init_cards(self):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Fort_Tent import Card_Tent
        from dominion.cards.Fort_Garrison import Card_Garrison
        from dominion.cards.Fort_Hill_Fort import Card_Hill_Fort
        from dominion.cards.Fort_Stronghold import Card_Stronghold

        self._cards = []
        for crd in (Card_Tent, Card_Garrison, Card_Hill_Fort, Card_Stronghold):
            for _ in range(4):
                self._cards.insert(0, crd())


###############################################################################
class Test_Forts(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_wizards(self):
        card = self.g["Forts"].remove()
        self.assertEqual(len(self.g["Forts"]), 15)
        self.assertEqual(card.name, "Tent")
        card = self.g["Forts"].remove()
        card = self.g["Forts"].remove()
        card = self.g["Forts"].remove()
        card = self.g["Forts"].remove()
        self.assertEqual(card.name, "Garrison")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

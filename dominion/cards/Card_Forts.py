#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Fort"""

import unittest
from dominion import Card, Game, CardPile


###############################################################################
class Card_Forts(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Forts"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = Card.CardType.ACTION

    def cardpile_setup(self, game):
        card_pile = FortCardPile(game)
        return card_pile


###############################################################################
class FortCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("Fort", game.paths["cards"], "Card_")
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Fort_Tent import Card_Tent
        from dominion.cards.Fort_Garrison import Card_Garrison
        from dominion.cards.Fort_Hill_Fort import Card_Hill_Fort
        from dominion.cards.Fort_Stronghold import Card_Stronghold

        for crd in (Card_Tent, Card_Garrison, Card_Hill_Fort, Card_Stronghold):
            for _ in range(4):
                self.cards.insert(0, crd())


###############################################################################
class TestForts(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forts"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_wizards(self):
        card = self.g.get_card_from_pile("Forts")
        self.assertEqual(len(self.g.card_piles["Forts"]), 15)
        self.assertEqual(card.name, "Tent")
        card = self.g.get_card_from_pile("Forts")
        card = self.g.get_card_from_pile("Forts")
        card = self.g.get_card_from_pile("Forts")
        card = self.g.get_card_from_pile("Forts")
        self.assertEqual(card.name, "Garrison")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

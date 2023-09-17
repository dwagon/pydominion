#!/usr/bin/env python

import unittest
from dominion import Card, Game, CardPile


###############################################################################
class Card_Augurs(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Augurs"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]
        self.numcards = 1

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = AugurCardPile(game)
        card_pile.init_cards()
        return card_pile


###############################################################################
class AugurCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("Augurs", game.paths["cards"], "Card_")
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Augur_Herb_Gatherer import Card_Herb_Gatherer
        from dominion.cards.Augur_Acolyte import Card_Acolyte
        from dominion.cards.Augur_Sorceress import Card_Sorceress
        from dominion.cards.Augur_Sibyl import Card_Sibyl

        for crd in (Card_Herb_Gatherer, Card_Acolyte, Card_Sorceress, Card_Sibyl):
            for _ in range(4):
                self.cards.insert(0, crd())


###############################################################################
class TestAugurs(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Augurs"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_augurs(self):
        card = self.g["Augurs"].remove()
        self.assertEqual(len(self.g["Augurs"]), 15)
        self.assertEqual(card.name, "Herb Gatherer")
        card = self.g["Augurs"].remove()
        card = self.g["Augurs"].remove()
        card = self.g["Augurs"].remove()
        card = self.g["Augurs"].remove()
        self.assertEqual(card.name, "Acolyte")
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Odyssey"""

import unittest
from dominion import Card, Game, CardPile, game_setup


###############################################################################
class Card_Odysseys(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Odysseys"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]
        self.numcards = 1

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = OdysseyCardPile(game)
        return card_pile


###############################################################################
class OdysseyCardPile(CardPile.CardPile):
    def __init__(self, game):
        mapping = game_setup.get_card_classes("Odyssey", game.paths["cards"], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Odyssey_Old_Map import Card_Old_Map
        from dominion.cards.Odyssey_Voyage import Card_Voyage
        from dominion.cards.Odyssey_Sunken_Treasure import Card_Sunken_Treasure
        from dominion.cards.Odyssey_Distant_Shore import Card_Distant_Shore

        for card in (
            Card_Old_Map,
            Card_Voyage,
            Card_Sunken_Treasure,
            Card_Distant_Shore,
        ):
            for _ in range(4):
                self.cards.insert(0, card())


###############################################################################
class TestOdysseys(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Odysseys"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_augurs(self):
        card = self.g.get_card_from_pile("Odysseys")
        self.assertEqual(len(self.g.card_piles["Odysseys"]), 15)
        self.assertEqual(card.name, "Old Map")
        card = self.g.get_card_from_pile("Odysseys")
        card = self.g.get_card_from_pile("Odysseys")
        card = self.g.get_card_from_pile("Odysseys")
        card = self.g.get_card_from_pile("Odysseys")
        self.assertEqual(card.name, "Voyage")
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

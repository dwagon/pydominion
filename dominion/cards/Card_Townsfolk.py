#!/usr/bin/env python

import unittest
from dominion import Card, Game, CardPile, game_setup, Keys


###############################################################################
class Card_Townsfolk(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Townsfolk"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]
        self.pile = "Townsfolk"

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = TownsfolkCardPile(game)
        return card_pile


###############################################################################
class TownsfolkCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game_setup.get_card_classes("Townsfolk", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in self.mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Townsfolk_Town_Crier import Card_Town_Crier
        from dominion.cards.Townsfolk_Blacksmith import Card_Blacksmith
        from dominion.cards.Townsfolk_Miller import Card_Miller
        from dominion.cards.Townsfolk_Elder import Card_Elder

        for card_class in (Card_Town_Crier, Card_Blacksmith, Card_Miller, Card_Elder):
            for _ in range(4):
                self.cards.insert(0, card_class())


###############################################################################
class Test_Townsfolk(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_wizards(self):
        card = self.g.get_card_from_pile("Townsfolk")
        self.assertEqual(len(self.g.card_piles["Townsfolk"]), 15)
        self.assertEqual(card.name, "Town Crier")
        card = self.g.get_card_from_pile("Townsfolk")
        card = self.g.get_card_from_pile("Townsfolk")
        card = self.g.get_card_from_pile("Townsfolk")
        card = self.g.get_card_from_pile("Townsfolk")
        self.assertEqual(card.name, "Blacksmith")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

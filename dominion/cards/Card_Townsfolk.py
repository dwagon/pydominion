#!/usr/bin/env python

import unittest
from dominion import Card, Game, CardPile


###############################################################################
class Card_Townsfolk(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Townsfolk"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]

    @classmethod
    def cardpile_setup(cls, game):
        return TownsfolkCardPile(game)


###############################################################################
class TownsfolkCardPile(CardPile.CardPile):
    def __init__(self, game, pile_size=10):
        self.mapping = game.getSetCardClasses("Townsfolk", game.cardpath, "dominions/cards", "Card_")
        super().__init__(cardname="Townsfolk", klass=None, game=game, pile_size=pile_size)

    def init_cards(self):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Townsfolk_Town_Crier import Card_Town_Crier
        from dominion.cards.Townsfolk_Blacksmith import Card_Blacksmith
        from dominion.cards.Townsfolk_Miller import Card_Miller
        from dominion.cards.Townsfolk_Elder import Card_Elder

        self._cards = []
        for crd in (Card_Town_Crier, Card_Blacksmith, Card_Miller, Card_Elder):
            for _ in range(4):
                self._cards.insert(0, crd())


###############################################################################
class Test_Townsfolk(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Townsfolk"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_wizards(self):
        card = self.g["Townsfolk"].remove()
        self.assertEqual(len(self.g["Townsfolk"]), 15)
        self.assertEqual(card.name, "Town Crier")
        card = self.g["Townsfolk"].remove()
        card = self.g["Townsfolk"].remove()
        card = self.g["Townsfolk"].remove()
        card = self.g["Townsfolk"].remove()
        self.assertEqual(card.name, "Blacksmith")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

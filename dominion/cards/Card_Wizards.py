#!/usr/bin/env python

import unittest
from dominion import Card, Game, CardPile


###############################################################################
class Card_Wizards(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Wizards"
        self.base = Game.ALLIES
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_LIAISON]
        self.required_cards = ["Curse"]

    def setup(self, game):
        game.cardpiles["Wizards"] = WizardCardPile(game)


###############################################################################
class WizardCardPile(CardPile.CardPile):
    def __init__(self, game, pile_size=10):
        self.mapping = game.getSetCardClasses(
            "Wizard", game.cardpath, "dominions/cards", "Card_"
        )
        super().__init__(cardname="Wizards", klass=None, game=game, pile_size=pile_size)

    def init_cards(self):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Wizard_Student import Card_Student
        from dominion.cards.Wizard_Conjurer import Card_Conjurer
        from dominion.cards.Wizard_Sorcerer import Card_Sorcerer
        from dominion.cards.Wizard_Lich import Card_Lich

        self._cards = []
        for crd in (Card_Student, Card_Conjurer, Card_Sorcerer, Card_Lich):
            for _ in range(4):
                self._cards.insert(0, crd())


###############################################################################
class Test_Wizard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"], use_liaisons=True)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_wizards(self):
        card = self.g["Wizards"].remove()
        self.assertEqual(len(self.g["Wizards"]), 15)
        self.assertEqual(card.name, "Student")
        card = self.g["Wizards"].remove()
        card = self.g["Wizards"].remove()
        card = self.g["Wizards"].remove()
        card = self.g["Wizards"].remove()
        self.assertEqual(card.name, "Conjurer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

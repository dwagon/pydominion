#!/usr/bin/env python

import unittest
from enum import auto
from dominion import Card, Game, CardPile


###############################################################################
class Card_Wizards(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Wizards"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = WizardCardPile(game)
        card_pile.init_cards()
        return card_pile


###############################################################################
class WizardCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("Wizard", game.paths["cards"], "Card_")
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Wizard_Student import Card_Student
        from dominion.cards.Wizard_Conjurer import Card_Conjurer
        from dominion.cards.Wizard_Sorcerer import Card_Sorcerer
        from dominion.cards.Wizard_Lich import Card_Lich

        for card_class in (Card_Student, Card_Conjurer, Card_Sorcerer, Card_Lich):
            for _ in range(4):
                self.cards.insert(0, card_class())


###############################################################################
class TestWizard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"])
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

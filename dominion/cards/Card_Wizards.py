#!/usr/bin/env python

import unittest
from dominion import Card, Game, CardPile, game_setup, Keys


###############################################################################
class Card_Wizards(Card.Card):
    def __init__(self) -> None:
        Card.Card.__init__(self)
        self.name = "Wizards"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]

    @classmethod
    def cardpile_setup(cls, game: Game.Game) -> "WizardCardPile":
        card_pile = WizardCardPile(game)
        return card_pile


###############################################################################
class WizardCardPile(CardPile.CardPile):
    def __init__(self, game: Game.Game) -> None:
        mapping = game_setup.get_card_classes("Wizard", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None) -> None:
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
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Wizards"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_wizards(self) -> None:
        card = self.g.get_card_from_pile("Wizards")
        self.assertEqual(len(self.g.card_piles["Wizards"]), 15)
        self.assertEqual(card.name, "Student")
        card = self.g.get_card_from_pile("Wizards")
        self.assertEqual(card.name, "Student")
        card = self.g.get_card_from_pile("Wizards")
        self.assertEqual(card.name, "Student")
        card = self.g.get_card_from_pile("Wizards")
        self.assertEqual(card.name, "Student")
        card = self.g.get_card_from_pile("Wizards")
        self.assertEqual(card.name, "Conjurer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

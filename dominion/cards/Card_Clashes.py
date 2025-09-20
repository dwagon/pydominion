#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Clashes"""

import unittest

from dominion import Card, Game, CardPile, game_setup, Keys


###############################################################################
class Card_Clashes(Card.Card):
    """Clashes"""

    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Clashes"
        self.base = Card.CardExpansion.ALLIES
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.required_cards = ["Curse"]

    @classmethod
    def cardpile_setup(cls, game):
        """Setup"""
        card_pile = ClashCardPile(game)
        return card_pile


###############################################################################
class ClashCardPile(CardPile.CardPile):
    """Pile of Clashes"""

    def __init__(self, game):
        mapping = game_setup.get_card_classes("Clash", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Clash_Battle_Plan import Card_BattlePlan
        from dominion.cards.Clash_Archer import Card_Archer
        from dominion.cards.Clash_Warlord import Card_Warlord
        from dominion.cards.Clash_Territory import Card_Territory

        for card in (Card_BattlePlan, Card_Archer, Card_Warlord, Card_Territory):
            for _ in range(4):
                self.cards.insert(0, card())


###############################################################################
class TestClashes(unittest.TestCase):
    """Test Clashes"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Clashes"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_clashes(self):
        """Test that we can rotate the pile"""
        card = self.g.get_card_from_pile("Clashes")
        self.assertEqual(len(self.g.card_piles["Clashes"]), 15)
        self.assertEqual(card.name, "Battle Plan")
        card = self.g.get_card_from_pile("Clashes")
        card = self.g.get_card_from_pile("Clashes")
        card = self.g.get_card_from_pile("Clashes")
        card = self.g.get_card_from_pile("Clashes")
        self.assertEqual(card.name, "Archer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

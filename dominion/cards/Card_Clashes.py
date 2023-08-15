#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Clashes """

import unittest
from dominion import Card, Game, Piles, CardPile


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
        return ClashCardPile(game)


###############################################################################
class ClashCardPile(CardPile.CardPile):
    """Pile of Clashes"""

    def __init__(self, game, pile_size=10):
        self.mapping = game.get_card_classes("Clashes", game.paths["cards"], "Clash_")
        super().__init__(cardname="Clashes", klass=None, game=game, pile_size=pile_size)

    def init_cards(self):
        # pylint: disable=import-outside-toplevel
        from dominion.cards.Clash_Battle_Plan import Card_Battle_Plan
        from dominion.cards.Clash_Archer import Card_Archer
        from dominion.cards.Clash_Warlord import Card_Warlord
        from dominion.cards.Clash_Territory import Card_Territory

        self._cards = []
        for crd in (Card_Battle_Plan, Card_Archer, Card_Warlord, Card_Territory):
            for _ in range(4):
                self._cards.insert(0, crd())


###############################################################################
class Test_Clashes(unittest.TestCase):
    """Text Clashes"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Clashes"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_clashes(self):
        """Test that we can rotate the pile"""
        card = self.g["Clashes"].remove()
        self.assertEqual(len(self.g["Clashes"]), 15)
        self.assertEqual(card.name, "Battle Plan")
        card = self.g["Clashes"].remove()
        card = self.g["Clashes"].remove()
        card = self.g["Clashes"].remove()
        card = self.g["Clashes"].remove()
        self.assertEqual(card.name, "Archer")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Castles"""
import unittest

from dominion import Game, Card, Piles, game_setup, Keys, CardPile


###############################################################################
class Card_Castles(Card.Card):
    """Castles"""

    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Castles"
        self.base = Card.CardExpansion.EMPIRES

    @classmethod
    def cardpile_setup(cls, game):
        """Setup castle pile"""
        card_pile = CastleCardPile(game)
        return card_pile


###############################################################################
class CastleCardPile(CardPile.CardPile):
    """Pile of Castles"""

    def __init__(self, game):
        self.mapping = game_setup.get_card_classes("Castle", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in self.mapping.items():
            game.card_instances[name] = class_()
        super().__init__()

    def init_cards(self, num_cards=0, card_class=None):
        self.cards = sorted([_() for _ in self.mapping.values()], key=lambda x: x.cost, reverse=True)


###############################################################################
class CastleCard(Card.Card):
    """Base class for Castle Cards"""


###############################################################################
class TestCastles(unittest.TestCase):
    """Test Castles"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Castles")
        self.plr.piles[Piles.HAND].set("Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)

    def test_castles(self):
        """TODO: Test"""
        self.g.print_state()


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

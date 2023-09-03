#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card
import dominion.CardPile as CardPile


###############################################################################
class Card_Castles(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Castles"
        self.base = Card.CardExpansion.EMPIRES

    def setup(self, game):
        game.cardpiles["Castles"] = CastleCardPile(game)


###############################################################################
class CastleCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("Castle", game.paths["cards"], "Card_")
        super().__init__()

    def init_cards(self):
        self.cards = sorted(
            [_() for _ in self.mapping.values()], key=lambda x: x.cost, reverse=True
        )


###############################################################################
class CastleCard(Card.Card):
    pass


###############################################################################
class Test_Castle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Castles"].remove()
        self.plr.piles[Piles.HAND].set("Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)

    def test_castles(self):
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

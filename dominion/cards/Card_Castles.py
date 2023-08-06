#!/usr/bin/env python

import unittest
import dominion.Game as Game
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
    def __init__(self, game, pile_size=10):
        self.mapping = game.getSetCardClasses(
            "Castle", game.cardpath, "dominions/cards", "Card_"
        )
        super().__init__(cardname="Castles", klass=None, game=game, pile_size=pile_size)

    def init_cards(self):
        self._cards = sorted(
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
        self.plr.hand.set("Silver", "Gold")
        self.plr.add_card(self.card, "hand")

    def test_castles(self):
        pass


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

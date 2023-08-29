#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Ruin """

import random
import unittest
from dominion import Card, CardPile, Game, Piles


###############################################################################
class Card_Ruin(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Ruins"
        self.base = Card.CardExpansion.DARKAGES

    def setup(self, game):
        game.cardpiles["Ruins"] = RuinCardPile(game)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return player.pick_to_discard(2)


###############################################################################
class RuinCardPile(CardPile.CardPile):
    def __init__(self, game):
        self.mapping = game.get_card_classes("RuinCard", game.paths["cards"], "Card_")
        super().__init__(
            klass=None,
            game=game,
        )

    #    def __getattr__(self, name):
    #        return getattr(self._cards[0], name)

    def init_cards(self):
        self._cards = [_() for _ in self.mapping.values()]
        random.shuffle(self._cards)


###############################################################################
class RuinCard(Card.Card):
    def __init__(self):
        self.name = "Undef Ruin"
        super().__init__()
        self.pile = "Ruins"


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

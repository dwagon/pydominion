#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Ruin"""

import random
import unittest

from dominion import Card, CardPile, game_setup, Keys


###############################################################################
class Card_Ruins(Card.Card):
    """Ruin"""

    def __init__(self):
        Card.Card.__init__(self)
        self.name = "Ruins"
        self.pile = "Ruins"
        self.base = Card.CardExpansion.DARKAGES

    @classmethod
    def cardpile_setup(cls, game):
        card_pile = RuinCardPile(game)
        return card_pile

    def calc_numcards(self, game):
        return max(10, game.numplayers * 10 - 10)


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover, pylint: disable=unused-argument
    return player.pick_to_discard(2)


###############################################################################
class RuinCardPile(CardPile.CardPile):
    """Ruin Card Pile"""

    def __init__(self, game):
        self.mapping = game_setup.get_card_classes("RuinCard", game_setup.PATHS[Keys.CARDS], "Card_")
        for name, class_ in self.mapping.items():
            game.card_instances[name] = class_()
        super().__init__(game=game)

    def init_cards(self, num_cards=0, card_class=None):
        for ruin_card in self.mapping.values():
            for _ in range(10):
                self.cards.append(ruin_card())
        random.shuffle(self.cards)
        self.cards = self.cards[:num_cards]


###############################################################################
class RuinsCard(Card.Card):
    def __init__(self):
        self.name = "Undef Ruin"
        super().__init__()
        self.pile = "Ruins"
        self.desc = "Ruin Card"


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

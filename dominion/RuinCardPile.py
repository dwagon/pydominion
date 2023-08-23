#!/usr/bin/env python
import random
from dominion.CardPile import CardPile


###############################################################################
class RuinCardPile(CardPile):
    def __init__(self, game, pile_size):
        self.mapping = game.get_card_classes("RuinCard", game.paths["cards"], "Card_")
        super().__init__(klass=None, game=game, pile_size=pile_size)

    def init_cards(self):
        for _ in range(self.pile_size):
            c = random.choice(list(self.mapping.keys()))
            self._cards.append(self.mapping[c]())


# EOF

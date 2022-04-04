#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Prize"""
from dominion import CardPile


###############################################################################
class PrizeCardPile(CardPile.CardPile):
    def __init__(self, cardname, game, pile_size):
        self.mapping = game.getSetCardClasses(
            "PrizeCard", game.cardpath, "domain/cards", "Card_"
        )
        super().__init__(cardname="Prizes", klass=self.mapping[cardname], game=game, pile_size=pile_size)


# EOF

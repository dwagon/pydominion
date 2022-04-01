#!/usr/bin/env python
from dominion import CardPile


###############################################################################
class PrizeCardPile(CardPile.CardPile):
    def __init__(self, cardname, klass):  # pylint: disable=super-init-not-called
        self.pilesize = 1
        self.cardname = cardname
        self.cardclass = klass
        self.card = klass()


# EOF

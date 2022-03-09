#!/usr/bin/env python
from dominion import CardPile


###############################################################################
class PrizeCardPile(CardPile.CardPile):
    def __init__(self, cardname, klass):  # pylint: disable=super-init-not-called
        self.pilesize = 1
        self.cardname = cardname
        self.cardclass = klass
        self.card = klass()

    #    def __getattr__(self, key):
    #        return getattr(self.prizes[-1], key)

    def remove(self):
        if self.pilesize:
            self.pilesize -= 1
            return self.cardclass()
        return None

    def __repr__(self):
        return "PrizeCardPile %s: %d" % (self.name, self.pilesize)


# EOF

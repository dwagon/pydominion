#!/usr/bin/env python
from CardPile import CardPile


###############################################################################
class PrizeCardPile(CardPile):
    def __init__(self, cardname, klass):
        self.numcards = 1
        self.cardname = cardname
        self.cardclass = klass
        self.card = klass()

#    def __getattr__(self, key):
#        return getattr(self.prizes[-1], key)

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.cardclass()
        else:
            return None

    def __repr__(self):
        return "PrizeCardPile %s: %d" % (self.name, self.numcards)


# EOF
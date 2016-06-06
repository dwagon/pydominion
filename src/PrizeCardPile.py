#!/usr/bin/env python
import random
from CardPile import CardPile


###############################################################################
class PrizeCardPile(CardPile):
    def __init__(self, mapping, numcards=1):
        self.numcards = numcards
        prizetypes = mapping

        self.prizes = []
        for i in range(numcards):
            c = random.choice(list(prizetypes.keys()))
            self.prizes.append(prizetypes[c]())

    def __getattr__(self, key):
        return getattr(self.prizes[-1], key)

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.prizes.pop()
        else:
            return None

    def __repr__(self):
        return "PrizeCardPile %s: %d" % (self.name, self.numcards)


###############################################################################
if __name__ == "__main__":
    r = PrizeCardPile()

# EOF

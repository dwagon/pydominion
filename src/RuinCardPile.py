#!/usr/bin/env python
import random
from CardPile import CardPile


###############################################################################
class RuinCardPile(CardPile):
    def __init__(self, mapping, pilesize=10):
        self.pilesize = pilesize
        ruintypes = mapping

        self.ruins = []
        for i in range(pilesize):
            c = random.choice(list(ruintypes.keys()))
            self.ruins.append(ruintypes[c]())

    def __getattr__(self, key):
        if key == 'card':
            return self.ruins[-1]
        return getattr(self.ruins[-1], key)

    def remove(self):
        if self.pilesize:
            self.pilesize -= 1
            return self.ruins.pop()
        else:
            return None

    def __repr__(self):
        return "RuinCardPile %s: %d" % (self.name, self.pilesize)


###############################################################################
if __name__ == "__main__":
    r = RuinCardPile()

# EOF

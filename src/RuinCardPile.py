#!/usr/bin/env python
import random
from CardPile import CardPile


###############################################################################
class RuinCardPile(CardPile):
    def __init__(self, mapping, numcards=10):
        self.numcards = numcards
        ruintypes = mapping

        self.ruins = []
        for i in range(numcards):
            c = random.choice(list(ruintypes.keys()))
            self.ruins.append(ruintypes[c]())

    def __getattr__(self, key):
        if key == 'card':
            return self.ruins[-1]
        return getattr(self.ruins[-1], key)

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.ruins.pop()
        else:
            return None

    def __repr__(self):
        return "RuinCardPile %s: %d" % (self.name, self.numcards)


###############################################################################
if __name__ == "__main__":
    r = RuinCardPile()

# EOF

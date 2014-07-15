#!/usr/bin/env python
import glob
import random
from CardPile import CardPile


###############################################################################
class RuinCardPile(CardPile):
    def __init__(self, numcards=10, cardpath='cards'):
        self.cardpath = cardpath
        self.numcards = numcards
        ruinfiles = glob.glob('%s/RuinCard_*.py' % cardpath)
        ruintypes = {}
        for r in ruinfiles:
            cardfile = r.replace('.py', '').replace('%s/' % cardpath, '')
            cardname = cardfile.replace('RuinCard_', '')
            ruintypes[cardname] = self.loadClass(cardname, cardfile)

        self.ruins = []
        for i in range(numcards):
            c = random.choice(values(ruintypes.keys()))
            self.ruins.append(ruintypes[c]())

    def __getattr__(self, key):
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

#EOF

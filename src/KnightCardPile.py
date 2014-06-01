#!/usr/bin/env python
import glob
import random
from CardPile import CardPile


###############################################################################
class KnightCardPile(CardPile):
    def __init__(self, numcards=10, cardpath='cards'):
        self.cardpath = cardpath
        self.numcards = numcards
        knightfiles = glob.glob('%s/KnightCard_*.py' % cardpath)
        knighttypes = {}
        for k in knightfiles:
            cardfile = k.replace('.py', '').replace('%s/' % cardpath, '')
            cardname = cardfile.replace('KnightCard_', '')
            knighttypes[cardname] = self.importCard(cardfile=cardfile, cardname=cardname)

        self.knights = []
        for i in range(numcards):
            c = random.choice(knighttypes.keys())
            self.knights.append(knighttypes[c])

    def remove(self):
        if self.numcards:
            self.numcards -= 1
            return self.knights.pop()
        else:
            return None

    def __repr__(self):
        return "KnightPile %s: %d" % (self.name, self.numcards)


###############################################################################
if __name__ == "__main__":
    k = KnightCardPile()

#EOF

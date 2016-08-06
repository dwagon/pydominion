import random
import sys


###############################################################################
class PlayArea(object):
    def __init__(self, initial=[]):
        self.cards = initial

    def __repr__(self):
        return "<PlayArea: %s>" % ", ".join([c.name for c in self.cards])

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        try:
            self.cards.remove(card)
        except ValueError:
            sys.stderr.write("Trying to remove a card (%s) that doesn't exist (%s)\n" % (card.name, ", ".join([c.name for c in self.cards])))
            raise

    def addToTop(self, card):
        self.cards.insert(0, card)

    def shuffle(self):
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def topcard(self):
        return self.cards.pop()

    def empty(self):
        self.cards = []

    def isEmpty(self):
        return self.cards == []

    def __eq__(self, a):
        if hasattr(a, 'cards'):
            return self.cards == a.cards
        else:
            return self.cards == a

    def __add__(self, a):
        x = self.cards[:]
        if hasattr(a, 'values'):
            x.extend(a.values())
        elif isinstance(a, PlayArea):
            x.extend(a.cards[:])
        return PlayArea(x)

    def __iter__(self):
        for c in self.cards:
            yield c

    def sort(self, *args, **kwargs):
        self.cards.sort(*args, **kwargs)

    def __getitem__(self, key):
        return self.cards[key]

# EOF

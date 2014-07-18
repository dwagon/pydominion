import random


###############################################################################
class PlayArea(object):
    def __init__(self, initial=[]):
        self.cards = initial

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

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

""" Class defining a PlayArea - such as a deck of cards, a player's hand of cards, etc """
import random
import sys
from dominion import Card
from dominion import CardPile
from dominion import Event
from dominion import BoonPile


###############################################################################
class PlayArea:
    def __init__(self, initial=None):
        if initial is None:
            initial = []
        self._cards = initial

    def __repr__(self):
        return "<PlayArea: %s>" % ", ".join([c.name for c in self._cards])

    def add(self, card):
        try:
            assert isinstance(
                card, (Card.Card, CardPile.CardPile, Event.EventPile, BoonPile.BoonPile)
            )
        except AssertionError:
            print(f"PlayArea.add({card=}) ({type(card)})")
            raise
        self._cards.append(card)

    def remove(self, card):
        try:
            self._cards.remove(card)
        except ValueError:
            sys.stderr.write(
                "Trying to remove a card (%s) that doesn't exist (%s)\n"
                % (card.name, ", ".join([c.name for c in self._cards]))
            )
            raise

    def addToTop(self, card):
        self._cards.insert(0, card)

    def shuffle(self):
        random.shuffle(self._cards)

    def size(self):
        return len(self)

    def __len__(self):
        return len(self._cards)

    def next_card(self):
        """ Take the next card of the playarea """
        return self._cards.pop()

    def top_card(self):
        """ Return the next card - but don't move it """
        return self._cards[0]

    def empty(self):
        self._cards = []

    def count(self, card):
        if hasattr(card, "name"):
            cname = card.name
        else:
            cname = card
        return [_.name for _ in self._cards].count(cname)

    def is_empty(self):
        return self._cards == []

    def __eq__(self, a):
        if hasattr(a, "cards"):
            return self._cards == a.cards
        return self._cards == a

    def __add__(self, a):
        x = self._cards[:]
        if a is None:
            pass
        elif hasattr(a, "values"):
            x.extend(a.values())
        elif isinstance(a, PlayArea):
            x.extend(a._cards[:])
        elif isinstance(a, list):
            x.extend(a[:])
        elif isinstance(a, Card.Card):
            x.append(a)
        else:
            sys.stderr.write("Unhandled __add__ operand: {}\n".format(type(a)))
        return PlayArea(x)

    def __iter__(self):
        for c in self._cards:
            yield c

    def sort(self, *args, **kwargs):
        self._cards.sort(*args, **kwargs)

    def __getitem__(self, key):
        return self._cards[key]

    ###########################################################################
    def dump(self, name):
        """Print out all of the playarea - for debugging purposes only"""
        print(f"---------- {name}")
        for crd in self._cards:
            print(f"Card={crd}")

# EOF

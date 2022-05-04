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

    ###########################################################################
    def __repr__(self):
        return f"<PlayArea: {', '.join([_.name for _ in self._cards])}>"

    ###########################################################################
    def __contains__(self, obj) -> bool:
        """Return True if a card {obj} or a card with name {obj} is in playarea"""
        for card in self._cards:
            if isinstance(obj, str):
                if card.name == obj:
                    return True
            elif card == obj:
                return True
        return False

    ###########################################################################
    def __getitem__(self, name_or_idx):
        """Return a card with the name {name_or_idx} or None from playarea
        If the {name_or_idx} is a integer - return that card from that index
        """
        if isinstance(name_or_idx, int):
            return self._cards[name_or_idx]
        for card in self._cards:
            if card.name == name_or_idx:
                return card
        return None

    ###########################################################################
    def add(self, card):
        try:
            assert isinstance(
                card, (Card.Card, CardPile.CardPile, Event.EventPile, BoonPile.BoonPile)
            )
        except AssertionError:
            print(f"PlayArea.add({card=}) ({type(card)})")
            raise
        self._cards.append(card)

    ###########################################################################
    def remove(self, card):
        try:
            self._cards.remove(card)
        except ValueError:
            sys.stderr.write(
                "Trying to remove a card (%s) that doesn't exist (%s)\n"
                % (card.name, ", ".join([c.name for c in self._cards]))
            )
            raise

    ###########################################################################
    def addToTop(self, card):
        self._cards.insert(0, card)

    ###########################################################################
    def shuffle(self):
        random.shuffle(self._cards)

    ###########################################################################
    def size(self):
        return len(self)

    ###########################################################################
    def __len__(self):
        return len(self._cards)

    ###########################################################################
    def next_card(self):
        """Take the next card of the playarea"""
        return self._cards.pop()

    ###########################################################################
    def top_card(self):
        """Return the next card - but don't move it"""
        return self._cards[0]

    ###########################################################################
    def empty(self):
        self._cards = []

    ###########################################################################
    def count(self, card):
        if hasattr(card, "name"):
            cname = card.name
        else:
            cname = card
        return [_.name for _ in self._cards].count(cname)

    ###########################################################################
    def is_empty(self):
        return self._cards == []

    ###########################################################################
    def __eq__(self, a):
        if hasattr(a, "cards"):
            return self._cards == a.cards
        return self._cards == a

    ###########################################################################
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
            sys.stderr.write(f"Unhandled __add__ operand: {type(a)}\n")
        return PlayArea(x)

    ###########################################################################
    def __iter__(self):
        for c in self._cards[:]:
            yield c

    ###########################################################################
    def sort(self, *args, **kwargs):
        self._cards.sort(*args, **kwargs)

    ###########################################################################
    def dump(self, name="PlayArea"):
        """Print out all of the playarea - for debugging purposes only"""
        print(f"-vvvvvvvv- {name}")
        for crd in self._cards:
            print(f"Card={crd}")
        print(f"-^^^^^^^^- {name}")


# EOF

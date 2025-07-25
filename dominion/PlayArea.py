"""Class defining a PlayArea - such as a deck of cards, a player's hand of cards, etc"""

import random
import sys
from typing import Any, Optional, Iterator, TYPE_CHECKING, Self

from dominion import NoCardException
from dominion.Card import Card

if TYPE_CHECKING:
    from dominion.Game import Game


###############################################################################
class PlayArea:
    """Area of play - such as a deck of cards"""

    def __init__(
        self,
        name: str = "",
        game: Optional["Game"] = None,
        initial: Optional[list[Card]] = None,
    ) -> None:
        self.name: str = name
        self.game: Optional[Game] = game
        if initial is None:
            initial = []
        self._cards: list[Card] = initial

    ###########################################################################
    def __repr__(self) -> str:
        return f"<PlayArea {self.name}: {', '.join([_.name for _ in self._cards])}>"

    ###########################################################################
    def __contains__(self, obj: Any) -> bool:
        """Return True if a card {obj} or a card with name {obj} is in play area"""
        for card in self._cards:
            if isinstance(obj, str):
                if card.name == obj:
                    return True
            elif card == obj:
                return True
        return False

    ###########################################################################
    def __getitem__(self, name_or_idx: str | int) -> Optional[Card]:
        """Return a card with the name {name_or_idx} or None from playarea
        If the {name_or_idx} is an integer - return that card from that index
        """
        if isinstance(name_or_idx, int):
            return self._cards[name_or_idx]
        for card in self._cards:
            if card.name == name_or_idx:
                return card
        return None

    ###########################################################################
    def set(self, *cards: str) -> None:
        """Used for testing to set contents"""
        self.empty()
        assert self.game is not None
        for card_name in cards:
            if card_name in self.game.card_piles:
                card = self.game.card_piles[card_name].remove()
            else:
                card = self.game.card_instances[card_name]
            if card is None:
                print(f"Card Pile {card_name} is empty")
                return
            if card.pile == "":
                card.pile = card_name
            card.location = self.name
            self.addToTop(card)

    ###########################################################################
    def add(self, card: Card) -> None:
        """Add a card to the area"""
        self._cards.insert(0, card)

    ###########################################################################
    def remove(self, card: Card) -> None:
        """Remove a card from the area"""
        try:
            self._cards.remove(card)
        except ValueError:
            sys.stderr.write(
                f"Trying to remove a card ({card}) that doesn't exist."
                f" Contents of {self.name} are: {', '.join([_.name for _ in self._cards])}\n"
            )
            raise

    ###########################################################################
    def addToTop(self, card: Card) -> None:
        self._cards.append(card)

    ###########################################################################
    def shuffle(self) -> None:
        random.shuffle(self._cards)

    ###########################################################################
    def size(self) -> int:
        return len(self)

    ###########################################################################
    def __len__(self) -> int:
        return len(self._cards)

    ###########################################################################
    def next_card(self) -> Card:
        """Take the next card of the play area"""
        return self._cards.pop()

    ###########################################################################
    def top_card(self) -> Card:
        """Return the next card - but don't move it"""
        try:
            return self._cards[-1]
        except IndexError as e:
            raise NoCardException from e

    ###########################################################################
    def empty(self) -> None:
        self._cards = []

    ###########################################################################
    def count(self, card: Card | str) -> int:
        cname = card.name if hasattr(card, "name") else card
        return [_.name for _ in self._cards].count(cname)

    ###########################################################################
    def is_empty(self) -> bool:
        return self._cards == []

    ###########################################################################
    def __eq__(self, a: Any) -> bool:
        return self._cards == a.cards if hasattr(a, "cards") else self._cards == a

    ###########################################################################
    def __add__(self, a: Any) -> Self:
        x = self._cards[:]
        if a is None:
            pass
        elif hasattr(a, "values"):
            x.extend(a.values())
        elif isinstance(a, PlayArea):
            x.extend(a._cards[:])
        elif isinstance(a, list):
            x.extend(a[:])
        elif isinstance(a, Card):
            x.append(a)
        else:
            sys.stderr.write(f"Unhandled __add__ operand: {type(a)}\n")
        return PlayArea("", self.game, x)

    ###########################################################################
    def __iter__(self) -> Iterator[Card]:
        for card in self._cards[:]:
            yield card

    ###########################################################################
    def sort(self, *args: Any, **kwargs: Any) -> None:
        self._cards.sort(*args, **kwargs)

    ###########################################################################
    def dump(self, name: Optional[str] = None) -> None:
        """Print out all the playarea - for debugging purposes only"""
        if name is None:
            name = self.name
        print(f"{name}: ", end="")
        for card in self._cards:
            print(f"{card} ", end="")
        print()


# EOF

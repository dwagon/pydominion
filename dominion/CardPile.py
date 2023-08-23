###############################################################################
from typing import Optional


class CardPile:
    def __init__(self, cardname, klass, game, pile_size=10):
        self.cardname = cardname
        self.cardclass = klass
        self.pile_size = pile_size
        self.game = game
        self._cards = []
        self.embargo_level = 0
        self._card = None
        if klass:
            self._card = klass()  # Non-playable instance to access card attributes
        self.init_cards()

    ###########################################################################
    def init_cards(self):
        """Create the cards in the pile - overwrite for funky piles"""
        if hasattr(self, "calc_numcards"):
            self.pile_size = self.calc_numcards(self.game)
        for _ in range(self.pile_size):
            self._cards.append(self.cardclass())

    ###########################################################################
    def __iter__(self):
        return CardPileIterator(self)

    ###########################################################################
    def add_to_pile(self, num):
        # Extend the pile
        for _ in range(num):
            self._cards.append(self.cardclass())

    ###########################################################################
    def __len__(self):
        return len(self._cards)

    ###########################################################################
    def __bool__(self):
        return not self.is_empty()

    ###########################################################################
    def embargo(self):
        self.embargo_level += 1

    ###########################################################################
    def __lt__(self, other_card):
        if self._card:
            self_name = self._card.name
        else:
            try:
                self_name = self._cards[-1].name
            except IndexError:
                self_name = "ZZZZ"
        if other_card._card:
            other_name = other_card._card.name
        else:
            try:
                other_name = other_card._cards[-1].name
            except IndexError:
                other_name = "ZZZZ"
        return self_name < other_name

    ###########################################################################
    def __getattr__(self, name):
        try:
            if self._card:
                return getattr(self._card, name)
            if self._cards:
                return getattr(self._cards[-1], name)
        except RecursionError:
            print(f"DBG {self.__class__.__name__}.__getattr__({name=})")
            raise
        except IndexError:
            print(
                f"DBG {self.__class__.__name__}.__getattr__({name=}) {self._card=} {self._cards=}"
            )
            raise

    ###########################################################################
    def is_empty(self):
        """Is the card pile empty"""
        return not self._cards

    ###########################################################################
    def remove(self):
        """Remove a card from the card pile"""
        try:
            return self._cards.pop()
        except IndexError:
            return None

    ###########################################################################
    def add(self, card):
        """Add a card to the bottom of the deck"""
        self._cards.insert(0, card)

    ###########################################################################
    def top_card(self) -> Optional[str]:
        """What is the top card of the card pile"""
        if self.is_empty():
            return None
        return self._cards[-1].name

    ###########################################################################
    def rotate(self):
        """Rotate a pile of cards - only works with split decks
        http://wiki.dominionstrategy.com/index.php/Rotate
        """
        if self.is_empty():
            return
        top_card_name = self.top_card()
        count = 0
        while True:
            count += 1
            if self.top_card() != top_card_name:
                break
            next_card = self.remove()
            self.add(next_card)
            if count > 20:  # Only one sort of card in deck
                break

    ###########################################################################
    def dump(self):
        """Print out all the pile - for debugging purposes only"""
        print("----------")
        for card in self._cards:
            print(f"Card={card}")

    ###########################################################################
    def __repr__(self):
        return f"<CardPile {self.name}: {len(self._cards)}>"


###############################################################################
class CardPileIterator:
    def __init__(self, card_pile):
        self.card_pile = card_pile
        self.index = 0

    def __next__(self):
        try:
            result = self.card_pile._cards[self.index]
        except IndexError:
            raise StopIteration  # pylint: disable=raise-missing-from
        self.index += 1
        return result


# EOF

###############################################################################
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dominion import Card


class CardPile:
    def __init__(self, game=None):
        # game is required by some subclasses
        self.cards = []
        self.embargo_level = 0
        self.gatheredvp = 0

    ###########################################################################
    def init_cards(self, num_cards=0, card_class=None):
        """Can be overwritten for the more unusual piles"""
        if num_cards == 0 or not card_class:
            return
        for _ in range(num_cards):
            self.cards.append(card_class())

    ##########################################################################
    def addVP(self, num=1):
        self.gatheredvp += num

    ##########################################################################
    def getVP(self):
        return self.gatheredvp

    ##########################################################################
    def drainVP(self):
        num = self.gatheredvp
        self.gatheredvp = 0
        return num

    ###########################################################################
    def __iter__(self):
        return CardPileIterator(self)

    ###########################################################################
    def __len__(self):
        return len(self.cards)

    ###########################################################################
    def __bool__(self):
        return not self.is_empty()

    ###########################################################################
    def embargo(self):
        self.embargo_level += 1

    ###########################################################################
    def __lt__(self, other_card):
        self_name = self.cards[-1].name
        if other_card.cards:
            other_name = other_card.cards[-1].name
        else:
            try:
                other_name = other_card.cards[-1].name
            except IndexError:
                other_name = "ZZZZ"
        return self_name < other_name

    ###########################################################################
    def setup(self, game):
        """Setup card pile"""
        if self.cards:
            self.cards[-1].setup(game)

    ###########################################################################
    def is_empty(self):
        """Is the card pile empty"""
        return not self.cards

    ###########################################################################
    def remove(self, name=""):
        """Remove a card from the card pile"""
        if not name:
            try:
                return self.cards.pop()
            except IndexError:
                return None
        for card in self.cards:
            if card.name == name:
                self.cards.remove(card)
                return card
        return None

    ###########################################################################
    def add(self, card):
        """Add a card to the bottom of the deck"""
        self.cards.insert(0, card)

    ###########################################################################
    def top_card(self) -> Optional[str]:
        """What is the name of the top card of the card pile"""
        # TODO: Make this return the card, not just the name
        if self.is_empty():
            return None
        return self.cards[-1].name

    ###########################################################################
    def get_top_card(self):
        """What is the top card of the card pile"""
        if self.is_empty():
            return None
        return self.cards[-1]

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
        for card in self.cards:
            print(f"Card={card}")

    ###########################################################################
    def __repr__(self):
        return f"<CardPile {len(self.cards)}>"


###############################################################################
class CardPileIterator:
    def __init__(self, card_pile):
        self.card_pile = card_pile
        self.index = 0

    def __next__(self):
        try:
            result = self.card_pile.cards[self.index]
        except IndexError:
            raise StopIteration  # pylint: disable=raise-missing-from
        self.index += 1
        return result


# EOF

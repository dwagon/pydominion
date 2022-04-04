###############################################################################
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
            self._card = klass()   # Non-playable instance to access card attributes
        self.init_cards()

    ###########################################################################
    def init_cards(self):
        """ Create the cards in the pile - overwrite for funky piles """
        for _ in range(self.pile_size):
            self._cards.append(self.cardclass())

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
    def __lt__(self, a):
        return self._cards[0].name < a._cards[0].name

    ###########################################################################
    def __getattr__(self, name):
        try:
            if self._card:
                return getattr(self._card, name)
            return getattr(self._cards[0], name)
        except RecursionError:
            print(f"DBG {self.__class__.__name__}.__getattr__({name=})")
            raise
        except IndexError:
            print(f"DBG {self.__class__.__name__}.__getattr__({name=}) {self._card=} {self._cards=}")
            raise

    ###########################################################################
    def is_empty(self):
        return not self._cards

    ###########################################################################
    def remove(self):
        try:
            return self._cards.pop()
        except IndexError:
            return None

    ###########################################################################
    def add(self, card):
        self._cards.insert(0, card)

    ###########################################################################
    def __repr__(self):
        return f"<CardPile {self.name}: {len(self._cards)}>"


# EOF

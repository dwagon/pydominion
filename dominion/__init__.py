from enum import auto, Enum, StrEnum


###############################################################################
class Piles(StrEnum):
    """Play Areas for a card"""

    HAND = auto()
    EXILE = auto()
    DURATION = auto()
    DEFER = auto()
    DECK = auto()
    PLAYED = auto()
    DISCARD = auto()
    RESERVE = auto()
    TRASH = auto()
    CARDPILE = auto()


###############################################################################
class Phase(Enum):
    """Phases of a players turn"""

    NONE = auto()
    START = auto()
    ACTION = auto()
    BUY = auto()
    NIGHT = auto()
    CLEANUP = auto()

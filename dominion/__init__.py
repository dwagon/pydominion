from enum import auto, Enum, StrEnum


###############################################################################
class NoCardException(Exception):
    """Player has run out of cards"""


###############################################################################
class Piles(StrEnum):
    """Play Areas for a card"""

    CARDPILE = auto()
    DECK = auto()
    DEFER = auto()
    DISCARD = auto()
    DURATION = auto()
    EXILE = auto()
    HAND = auto()
    PLAYED = auto()
    RESERVE = auto()
    TRASH = auto()


###############################################################################
class Phase(Enum):
    """Phases of a players turn"""

    NONE = auto()
    START = auto()
    ACTION = auto()
    BUY = auto()
    NIGHT = auto()
    CLEANUP = auto()


###############################################################################
class Keys(StrEnum):
    """Keys to various internal arrays- to stop using magic strings as dictionary keys"""

    ALLIES = auto()
    ARTIFACTS = auto()
    BAD_CARDS = auto()
    BOONS = auto()
    CARDS = auto()
    EVENT = auto()
    HEXES = auto()
    LANDMARK = auto()
    LOOT = auto()
    PROJECTS = auto()
    STATES = auto()
    TRAITS = auto()
    WAY = auto()


###############################################################################
class Limits(StrEnum):
    """Limits to play"""

    PLAY = auto()
    BUY = auto()


###############################################################################
class Whens(StrEnum):
    """When a card can be called"""

    ANY = auto()
    POSTACTION = auto()
    SPECIAL = auto()
    START = auto()


# EOF

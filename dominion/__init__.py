"""Constants used in many places"""

from enum import auto, Enum, StrEnum

from dominion.Option import Option


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
    SPECIAL = auto()
    TOPDECK = auto()  # Not a real location, but the DECK
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
    BASE_CARDS = auto()
    BOONS = auto()
    CARDS = auto()
    CASTLE = auto()
    EVENT = auto()
    HEIRLOOM = auto()
    HEXES = auto()
    LANDMARK = auto()
    LOOT = auto()
    PRIZE = auto()
    PROJECTS = auto()
    PROPHECIES = auto()
    SHELTERS = auto()
    SPLIT = auto()
    STATES = auto()
    TRAITS = auto()
    TRAVELLER = auto()
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


###############################################################################
class OptionKeys(StrEnum):
    """Keys for option returns"""

    DESTINATION = auto()
    DISCARD = auto()
    DISCARD_PLAYED = auto()
    DONTADD = auto()
    EXILE = auto()
    REPLACE = auto()
    SHUFFLE = auto()
    SKIP_CARD = auto()
    TRASH = auto()


###############################################################################
class Token(StrEnum):
    """Tokens"""

    PLUS_1_ACTION = "+1 Action"
    PLUS_1_BUY = "+1 Buy"
    PLUS_1_COIN = "+1 Coin"
    PLUS_1_CARD = "+1 Card"
    MINUS_2_COST = "-2 Cost"
    TRASHING = "Trashing"
    MINUS_1_CARD = "-1 Card"
    MINUS_1_COIN = "-1 Coin"
    JOURNEY = "Journey"
    ESTATE = "Estate"


###############################################################################
class Action(StrEnum):
    """Types of actions that can be taken"""

    BUY = auto()
    EVENT = auto()
    PROJECT = auto()
    RESERVE = auto()
    COFFER = auto()
    VILLAGER = auto()
    PLAY = auto()
    SPEND = auto()
    PAYBACK = auto()
    SPENDALL = auto()
    QUIT = auto()
    WAY = auto()
    NONE = auto()


# EOF

""" The master class for all cards """
# pylint: disable=no-member

import uuid
from enum import Enum, auto


###############################################################################
class CardExpansion(Enum):
    """Source of the various cards"""

    ADVENTURE = auto()
    ALCHEMY = auto()
    ALLIES = auto()
    CORNUCOPIA = auto()
    DARKAGES = auto()
    DOMINION = auto()
    EMPIRES = auto()
    GUILDS = auto()
    HINTERLANDS = auto()
    INTRIGUE = auto()
    MENAGERIE = auto()
    NOCTURNE = auto()
    PROMO = auto()
    PROSPERITY = auto()
    RENAISSANCE = auto()
    SEASIDE = auto()


###############################################################################
class CardType(Enum):
    """Type of card"""

    ACTION = auto()
    ALLY = auto()
    ARTIFACT = auto()
    ATTACK = auto()
    AUGUR = auto()
    BOON = auto()
    CASTLE = auto()
    CLASH = auto()
    COMMAND = auto()
    DOOM = auto()
    DURATION = auto()
    FATE = auto()
    FORT = auto()
    GATHERING = auto()
    HEIRLOOM = auto()
    HEX = auto()
    KNIGHT = auto()
    LIAISON = auto()
    LOOTER = auto()
    NIGHT = auto()
    ODYSSEY = auto()
    PRIZE = auto()
    PROJECT = auto()
    REACTION = auto()
    RESERVE = auto()
    RUIN = auto()
    SHELTER = auto()
    SPIRIT = auto()
    STATE = auto()
    TOWNSFOLK = auto()
    TRAVELLER = auto()
    TREASURE = auto()
    VICTORY = auto()
    WIZARD = auto()
    ZOMBIE = auto()


##############################################################################
##############################################################################
##############################################################################
class Card:
    """Card class"""

    def __init__(self):
        self.basecard = False
        self.cost = -1
        self.debtcost = 0
        self.always_buyable = False
        self.potcost = False
        self.cardtype = "unknown"
        self.purchasable = True
        self.permanent = False
        self.playable = True
        self.callable = True
        self.defense = False
        self.needsprize = False
        self.needsartifacts = False
        self.needsprojects = False
        self.overpay = False
        self.insupply = True
        self.traveller = False
        self.when = "any"
        self.actions = 0
        self.buys = 0
        self.favors = 0
        self.coin = 0
        self.potion = 0
        self.cards = 0
        self.victory = 0
        self.required_cards = []
        self.image = None
        self.numcards = 10
        self.gatheredvp = 0
        self.retain_boon = False
        self.heirloom = None
        self.uuid = uuid.uuid4().hex
        self._location = None
        self._player = None

    ##########################################################################
    def check(self):
        """Check for some basic validity
        Some of these checks are caused by inconsistent naming standards
        """
        if not hasattr(self, "base"):
            raise NotImplementedError(f"{self.__class__.__name__} has no base")
        if not hasattr(self, "name"):
            raise NotImplementedError(f"{self.__class__.__name__} has no name")
        if hasattr(self, "coins"):
            raise NotImplementedError(f"{self.__class__.__name__} has coins not coin")
        if hasattr(self, "action"):
            raise NotImplementedError(f"{self.__class__.__name__} has action not actions")
        if hasattr(self, "potions"):
            raise NotImplementedError(f"{self.__class__.__name__} has potions not potion")
        if hasattr(self, "card"):
            raise NotImplementedError(f"{self.__class__.__name__} has card not cards")
        if hasattr(self, "buy"):
            raise NotImplementedError(f"{self.__class__.__name__} has buy not buys")

    ##########################################################################
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        self._location = val

    ##########################################################################
    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, val):
        self._player = val

    ##########################################################################
    def get_cardtype_repr(self):
        if isinstance(self.cardtype, list):
            ct = self.cardtype[:]
        else:
            ct = [self.cardtype]
        try:
            return ", ".join([_.name.title() for _ in ct])
        except AttributeError:
            print(f"DBG {self}")
            print(f"DBG {ct}")
            raise

    ##########################################################################
    def __repr__(self):
        return f"{self.name} {self.uuid} {self._player}@{self._location}"

    ##########################################################################
    def __lt__(self, card):
        return self.name < card.name

    ##########################################################################
    def description(self, player):
        if callable(self.desc):
            return self.desc(player)
        return self.desc

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

    ##########################################################################
    def special(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def night(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def duration(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def setup(self, game):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def has_defense(self):
        """Hook - overwritten in subclasses"""
        return self.defense

    ##########################################################################
    def isLiaison(self):
        """Is this card a Liaison
        http://wiki.dominionstrategy.com/index.php/Liaison"""
        return self._is_type(CardType.LIAISON)

    ##########################################################################
    def isGathering(self):
        return self._is_type(CardType.GATHERING)

    ##########################################################################
    def isCommand(self):
        """http://wiki.dominionstrategy.com/index.php/Command"""
        return self._is_type(CardType.COMMAND)

    ##########################################################################
    def isDuration(self):
        return self._is_type(CardType.DURATION)

    ##########################################################################
    def isDebt(self):
        return self.debtcost != 0

    ##########################################################################
    def isTreasure(self):
        return self._is_type(CardType.TREASURE)

    ##########################################################################
    def isNight(self):
        return self._is_type(CardType.NIGHT)

    ##########################################################################
    def isFate(self):
        """Is the card a Fate"""
        return self._is_type(CardType.FATE)

    ##########################################################################
    def isDoom(self):
        """Is the card a Doom"""
        return self._is_type(CardType.DOOM)

    ##########################################################################
    def isLooter(self):
        """Is the card a Looter"""
        return self._is_type(CardType.LOOTER)

    ##########################################################################
    def _is_type(self, ctype):
        """Is the card a specific type"""
        if isinstance(self.cardtype, list):
            if ctype in self.cardtype:
                return True
        else:
            if ctype == self.cardtype:
                return True
        return False

    ##########################################################################
    def isAction(self):
        """http://wiki.dominionstrategy.com/index.php/Action"""
        return self._is_type(CardType.ACTION)

    ##########################################################################
    def isShelter(self):
        """http://wiki.dominionstrategy.com/index.php/Shelter"""
        return self._is_type(CardType.SHELTER)

    ##########################################################################
    def isRuin(self):
        """http://wiki.dominionstrategy.com/index.php/Ruin"""
        return self._is_type(CardType.RUIN)

    ##########################################################################
    def isTraveller(self):
        """http://wiki.dominionstrategy.com/index.php/Traveller"""
        return self._is_type(CardType.TRAVELLER)

    ##########################################################################
    def isVictory(self):
        """http://wiki.dominionstrategy.com/index.php/Victory"""
        return self._is_type(CardType.VICTORY)

    ##########################################################################
    def isReaction(self):
        """http://wiki.dominionstrategy.com/index.php/Reaction"""
        return self._is_type(CardType.REACTION)

    ##########################################################################
    def isCastle(self):
        """http://wiki.dominionstrategy.com/index.php/Castle"""
        return self._is_type(CardType.CASTLE)

    ##########################################################################
    def isKnight(self):
        """http://wiki.dominionstrategy.com/index.php/Knight"""
        return self._is_type(CardType.KNIGHT)

    ##########################################################################
    def isAttack(self):
        """http://wiki.dominionstrategy.com/index.php/Attack"""
        return self._is_type(CardType.ATTACK)

    ##########################################################################
    def isReserve(self):
        """http://wiki.dominionstrategy.com/index.php/Reserve"""
        return self._is_type(CardType.RESERVE)

    ##########################################################################
    def special_score(self, game, player):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return 0  # pragma: nocover

    ##########################################################################
    def hook_cleanup(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_all_players_pre_action(self, game, player, owner, card):
        """Hook - overwritten in subclasses if required"""

    ##########################################################################
    def hook_pre_action(self, game, player, card):
        """Hook - overwritten in subclasses if required"""

    ##########################################################################
    def hook_all_players_buy_card(self, game, player, owner, card):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_buy_card(self, game, player, card):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_buy_this_card(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_call_reserve(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_allowed_to_buy(self, game, player):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return True  # pragma: no cover

    ##########################################################################
    def hook_allplayers_gain_card(self, game, player, owner, card):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_gain_card(self, game, player, card):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return {}  # pragma: no cover

    ##########################################################################
    def hook_card_cost(self, game, player, card):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return 0  # pragma: no cover

    ##########################################################################
    def hook_this_card_cost(self, game, player):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return 0  # pragma: no cover

    ##########################################################################
    def hook_coinvalue(self, game, player):
        """Hook - overwritten in subclasses;
        How much coin does this card contribute"""
        return self.coin  # pragma: no cover

    ##########################################################################
    def hook_spend_value(self, game, player, card):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses
        Does this card make any  modifications on the value of spending a card"""
        return 0  # pragma: no cover

    ##########################################################################
    def hook_underAttack(self, game, player, attacker):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_discard_this_card(self, game, player, source):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_trashThisCard(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_trash_card(self, game, player, card):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_gain_this_card(self, game, player):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return {}  # pragma: no cover

    ##########################################################################
    def hook_end_turn(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_end_of_game(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_pre_buy(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_end_buy_phase(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_start_turn(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_revealThisCard(self, game, player):
        """Hook - overwritten in subclasses"""


# EOF

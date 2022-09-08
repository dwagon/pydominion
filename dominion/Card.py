""" The master class for all cards """
# pylint: disable=no-member

import uuid

TYPE_ACTION = "action"
TYPE_ALLY = "ally"
TYPE_ARTIFACT = "artifact"
TYPE_ATTACK = "attack"
TYPE_BOON = "boon"
TYPE_CASTLE = "castle"
TYPE_COMMAND = "command"
TYPE_DOOM = "doom"
TYPE_DURATION = "duration"
TYPE_FATE = "fate"
TYPE_GATHERING = "gathering"
TYPE_HEIRLOOM = "heirloom"
TYPE_HEX = "hex"
TYPE_KNIGHT = "knight"
TYPE_LIAISON = "liaison"
TYPE_LOOTER = "looter"
TYPE_NIGHT = "night"
TYPE_PRIZE = "prize"
TYPE_PROJECT = "project"
TYPE_REACTION = "reaction"
TYPE_RESERVE = "reserve"
TYPE_RUIN = "ruin"
TYPE_SHELTER = "shelter"
TYPE_SPIRIT = "spirit"
TYPE_STATE = "state"
TYPE_TRAVELLER = "traveller"
TYPE_TREASURE = "treasure"
TYPE_VICTORY = "victory"
TYPE_ZOMBIE = "zombie"


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
        if isinstance(self.cardtype, str):
            ct = [self.cardtype]
        else:
            ct = self.cardtype[:]
        return ", ".join([_.title() for _ in ct])

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
        if TYPE_LIAISON in self.cardtype:
            return True
        return False

    ##########################################################################
    def isGathering(self):
        if TYPE_GATHERING in self.cardtype:
            return True
        return False

    ##########################################################################
    def isCommand(self):
        """http://wiki.dominionstrategy.com/index.php/Command"""
        if TYPE_COMMAND in self.cardtype:
            return True
        return False

    ##########################################################################
    def isDuration(self):
        if TYPE_DURATION in self.cardtype:
            return True
        return False

    ##########################################################################
    def isDebt(self):
        return self.debtcost != 0

    ##########################################################################
    def isTreasure(self):
        if TYPE_TREASURE in self.cardtype:
            return True
        return False

    ##########################################################################
    def isNight(self):
        if TYPE_NIGHT in self.cardtype:
            return True
        return False

    ##########################################################################
    def isFate(self):
        if TYPE_FATE in self.cardtype:
            return True
        return False

    ##########################################################################
    def isDoom(self):
        if TYPE_DOOM in self.cardtype:
            return True
        return False

    ##########################################################################
    def isLooter(self):
        if TYPE_LOOTER in self.cardtype:
            return True
        return False

    ##########################################################################
    def isAction(self):
        if TYPE_ACTION in self.cardtype:
            return True
        return False

    ##########################################################################
    def isShelter(self):
        if TYPE_SHELTER in self.cardtype:
            return True
        return False

    ##########################################################################
    def isRuin(self):
        if TYPE_RUIN in self.cardtype:
            return True
        return False

    ##########################################################################
    def isTraveller(self):
        if TYPE_TRAVELLER in self.cardtype:
            return True
        return False

    ##########################################################################
    def isVictory(self):
        if TYPE_VICTORY in self.cardtype:
            return True
        return False

    ##########################################################################
    def isReaction(self):
        if TYPE_REACTION in self.cardtype:
            return True
        return False

    ##########################################################################
    def isCastle(self):
        if TYPE_CASTLE in self.cardtype:
            return True
        return False

    ##########################################################################
    def isKnight(self):
        if TYPE_KNIGHT in self.cardtype:
            return True
        return False

    ##########################################################################
    def isAttack(self):
        if TYPE_ATTACK in self.cardtype:
            return True
        return False

    ##########################################################################
    def isReserve(self):
        if TYPE_RESERVE in self.cardtype:
            return True
        return False

    ##########################################################################
    def special_score(self, game, player):  # pylint: disable=no-self-use
        """Hook - overwritten in subclasses"""
        return 0  # pragma: nocover

    ##########################################################################
    def hook_cleanup(self, game, player):
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_all_players_pre_action(self, game, player, owner, card):
        """Hook - overwritten in subclasses"""

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

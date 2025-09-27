"""The master class for all cards"""

# pylint: disable=no-member

import os
import uuid
from enum import Enum, auto
from typing import Optional, TYPE_CHECKING, Any, Union

from dominion import Piles, Whens, OptionKeys

if TYPE_CHECKING:
    from dominion import Game, Player, PlayArea


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
    PLUNDER = auto()
    PROMO = auto()
    PROSPERITY = auto()
    RENAISSANCE = auto()
    SEASIDE = auto()
    CORNUCOPIA_GUILDS = auto()
    RISING_SUN = auto()
    TEST = auto()


###############################################################################
class CardType(Enum):
    """Type of card"""

    UNDEFINED = auto()
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
    LOOT = auto()
    LOOTER = auto()
    NIGHT = auto()
    ODYSSEY = auto()
    OMEN = auto()
    PRIZE = auto()
    PROJECT = auto()
    REACTION = auto()
    RESERVE = auto()
    RUIN = auto()
    SHADOW = auto()
    SHELTER = auto()
    SPIRIT = auto()
    STATE = auto()
    TOWNSFOLK = auto()
    TRAITS = auto()
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

    def __init__(self) -> None:
        self.name = ""
        self.basecard = False
        self.cost = -1
        self.debtcost = 0
        self.always_buyable = False
        self.potcost = False
        self.cardtype: CardType | list[CardType] = CardType.UNDEFINED
        self.purchasable = True
        self.permanent = False
        self.playable = True
        self.callable = True
        self.defense = False
        self.needs_prizes = False
        self.needsartifacts = False
        self.needsprojects = False
        self.overpay = False
        self.insupply = True
        self.traveller = False
        self.when = Whens.ANY
        self.actions = 0
        self.buys = 0
        self.favors = 0
        self.coin = 0
        self.potion = 0
        self.cards = 0
        self.victory = 0
        self.required_cards: list[str | tuple[str, str]] = []
        self.image = None
        self.numcards = 10
        self.retain_boon = False
        self.heirloom: Optional[str] = None
        self.uuid = uuid.uuid4().hex
        self._location: Optional[Piles] = None
        self._player: Optional[Player.Player] = None
        self._pile: str = ""
        self.desc: str = ""
        self.base: CardExpansion = CardExpansion.TEST

    ##########################################################################
    @property
    def pile(self) -> str:
        if not self._pile:
            return self.name
        return self._pile

    @pile.setter
    def pile(self, value: str) -> None:
        self._pile = value

    ##########################################################################
    def check(self) -> None:
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
    def location(self) -> Optional[Piles]:
        return self._location

    @location.setter
    def location(self, val: Optional[Piles]) -> None:
        self._location = val

    ##########################################################################
    @property
    def player(self) -> Optional["Player.Player"]:
        return self._player

    @player.setter
    def player(self, val: Optional["Player.Player"]) -> None:
        self._player = val

    ##########################################################################
    def get_cardtype_repr(self) -> str:
        if isinstance(self.cardtype, list):
            ct = self.cardtype[:]
        else:
            ct = [self.cardtype]

        return ", ".join([_.name.title() for _ in ct])

    ##########################################################################
    def __repr__(self) -> str:
        if os.getenv("PYDOMINION_DEBUG"):
            return f"{self.name} ({self.uuid} {self._player}@{self._location})"
        return f"{self.name}"

    ##########################################################################
    def __lt__(self, card: "Card") -> bool:
        assert isinstance(card, Card), f"__lt__({card=}) {type(card)=}"
        return self.name < card.name

    ##########################################################################
    def description(self, player: "Player.Player") -> str:
        if desc := self.dynamic_description(player):
            ans = desc
        else:
            ans = self.desc
        for card in player.relevant_cards():
            if additional := card.hook_card_description(player.game, player, self):
                ans += f" {additional}"
        for card in list(player.game.events.values()) + list(player.game.traits.values()):
            if additional := card.hook_all_card_description(player.game, player, self):
                ans += f" {additional}"
        return ans

    ##########################################################################
    def hook_card_description(self, game: "Game.Game", player: "Player.Player", card: "Card") -> str:
        """Hook to return additional details for a card"""
        return ""

    ##########################################################################
    def hook_all_card_description(self, game: "Game.Game", player: "Player.Player", card: "Card") -> str:
        """Hook to return additional details for a card based on all cards in the game"""
        return ""

    ##########################################################################
    def dynamic_description(self, player: "Player.Player") -> str:
        """Dynamic description - generally based on phase"""
        return ""

    ##########################################################################
    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_overpay(self, game: "Game.Game", player: "Player.Player", amount: int) -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def night(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def duration(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, str]:
        """Hook - overwritten in subclasses"""
        return {}

    ##########################################################################
    def setup(self, game: "Game.Game") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def has_defense(self) -> bool:
        """Hook - overwritten in subclasses"""
        return self.defense

    ##########################################################################
    def isLiaison(self) -> bool:
        """Is this card a Liaison
        http://wiki.dominionstrategy.com/index.php/Liaison"""
        return self._is_type(CardType.LIAISON)

    ##########################################################################
    def isGathering(self) -> bool:
        return self._is_type(CardType.GATHERING)

    ##########################################################################
    def isOmen(self) -> bool:
        return self._is_type(CardType.OMEN)

    ##########################################################################
    def isCommand(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Command"""
        return self._is_type(CardType.COMMAND)

    ##########################################################################
    def isDuration(self) -> bool:
        return self._is_type(CardType.DURATION)

    ##########################################################################
    def isDebt(self) -> bool:
        return self.debtcost != 0

    ##########################################################################
    def isTreasure(self) -> bool:
        return self._is_type(CardType.TREASURE)

    ##########################################################################
    def isNight(self) -> bool:
        return self._is_type(CardType.NIGHT)

    ##########################################################################
    def isFate(self) -> bool:
        """Is the card a Fate"""
        return self._is_type(CardType.FATE)

    ##########################################################################
    def isDoom(self) -> bool:
        """Is the card a Doom"""
        return self._is_type(CardType.DOOM)

    ##########################################################################
    def isLooter(self) -> bool:
        """Is the card a Looter"""
        return self._is_type(CardType.LOOTER)

    ##########################################################################
    def _is_type(self, ctype: CardType) -> bool:
        """Is the card a specific type"""
        if isinstance(self.cardtype, list):
            if ctype in self.cardtype:
                return True
        else:
            if ctype == self.cardtype:
                return True
        return False

    ##########################################################################
    def isAction(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Action"""
        return self._is_type(CardType.ACTION)

    ##########################################################################
    def isLoot(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Loot"""
        return self._is_type(CardType.LOOT)

    ##########################################################################
    def isShelter(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Shelter"""
        return self._is_type(CardType.SHELTER)

    ##########################################################################
    def isRuin(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Ruin"""
        return self._is_type(CardType.RUIN)

    ##########################################################################
    def isTraveller(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Traveller"""
        return self._is_type(CardType.TRAVELLER)

    ##########################################################################
    def isVictory(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Victory"""
        return self._is_type(CardType.VICTORY)

    ##########################################################################
    def isReaction(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Reaction"""
        return self._is_type(CardType.REACTION)

    ##########################################################################
    def isCastle(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Castle"""
        return self._is_type(CardType.CASTLE)

    ##########################################################################
    def isKnight(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Knight"""
        return self._is_type(CardType.KNIGHT)

    ##########################################################################
    def isAttack(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Attack"""
        return self._is_type(CardType.ATTACK)

    ##########################################################################
    def isReserve(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Reserve"""
        return self._is_type(CardType.RESERVE)

    ##########################################################################
    def isShadow(self) -> bool:
        """http://wiki.dominionstrategy.com/index.php/Shadow"""
        return self._is_type(CardType.SHADOW)

    ##########################################################################
    def special_score(self, game: "Game.Game", player: "Player.Player") -> int:
        """Hook - overwritten in subclasses"""
        return 0  # pragma: nocover

    ##########################################################################
    def hook_cleanup(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}

    ##########################################################################
    def hook_all_players_pre_play(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card",
    ) -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses if required"""
        return {}

    ##########################################################################
    def hook_all_players_post_play(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card",
    ) -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses if required"""
        return {}

    ##########################################################################
    def hook_pre_play(self, game: "Game.Game", player: "Player.Player", card: "Card") -> dict[OptionKeys, str]:
        """Hook - overwritten in subclasses if required"""
        return {}

    ##########################################################################
    def hook_post_play(self, game: "Game.Game", player: "Player.Player", card: "Card") -> dict[OptionKeys, str]:
        """Called after a card is played"""
        return {}

    ##########################################################################
    def hook_all_players_buy_card(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card",
    ) -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_buy_card(self, game: "Game.Game", player: "Player.Player", card: "Card") -> None:
        """Hook - overwritten in subclasses"""
        return None

    ##########################################################################
    def hook_buy_this_card(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_call_reserve(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_allowed_to_buy(self, game: "Game.Game", player: "Player.Player") -> bool:
        """Hook - overwritten in subclasses"""
        return True  # pragma: no cover

    ##########################################################################
    def hook_all_players_gain_card(
        self,
        game: "Game.Game",
        player: "Player.Player",
        owner: "Player.Player",
        card: "Card",
    ) -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}

    ##########################################################################
    def hook_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card") -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}  # pragma: no cover

    ##########################################################################
    def hook_card_cost(self, game: "Game.Game", player: "Player.Player", card: "Card") -> int:
        """Hook - overwritten in subclasses"""
        return 0  # pragma: no cover

    ##########################################################################
    def hook_this_card_cost(self, game: "Game.Game", player: "Player.Player") -> int:
        """Hook - overwritten in subclasses"""
        return 0  # pragma: no cover

    ##########################################################################
    def hook_coinvalue(self, game: "Game.Game", player: "Player.Player") -> int:
        """Hook - overwritten in subclasses;
        How much coin does this card contribute"""
        return self.coin  # pragma: no cover

    ##########################################################################
    def hook_spend_value(self, game: "Game.Game", player: "Player.Player", card: "Card") -> int:
        """Hook - overwritten in subclasses
        Does this card make any  modifications on the value of spending a card"""
        return 0  # pragma: no cover

    ##########################################################################
    def hook_under_attack(self, game: "Game.Game", player: "Player.Player", attacker: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_discard_this_card(
        self, game: "Game.Game", player: "Player.Player", source: Optional[Union[Piles, "PlayArea.PlayArea"]]
    ) -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_discard_any_card(self, game: "Game.Game", player: "Player.Player", card: "Card") -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}

    ##########################################################################
    def hook_trash_this_card(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}

    ##########################################################################
    def hook_trash_card(self, game: "Game.Game", player: "Player.Player", card: "Card") -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}

    ##########################################################################
    def hook_gain_this_card(self, game: "Game.Game", player: "Player.Player") -> dict[OptionKeys, Any]:
        """Hook - overwritten in subclasses"""
        return {}  # pragma: no cover

    ##########################################################################
    def hook_end_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_end_of_game(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_pre_buy(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_end_buy_phase(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_start_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_start_every_turn(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook fired every turn if this card is in the game - overwritten in subclasses"""

    ##########################################################################
    def hook_reveal_this_card(self, game: "Game.Game", player: "Player.Player") -> None:
        """Hook - overwritten in subclasses"""

    ##########################################################################
    def hook_reveal_prophecy(self, game: "Game.Game") -> None:
        """Prophecy is revealed for the first time"""

    ##########################################################################
    def debug_dump(self, player: "Player.Player") -> None:
        """Dump any debug info"""
        return

    ##########################################################################
    def hook_any_gain_card(self, game: "Game.Game", player: "Player.Player", card: "Card") -> dict[OptionKeys, Any]:
        """Call this for every card in the game whether in play or not"""
        return {}

    ##########################################################################
    def hook_emptied_pile(self, game: "Game.Game", player: "Player.Player", card: "Card") -> None:
        """A card pile has been emptied"""

    ##########################################################################
    def hook_pre_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """About to shuffle the deck"""

    ##########################################################################
    def hook_post_shuffle(self, game: "Game.Game", player: "Player.Player") -> None:
        """Just finished shuffling the deck"""


# EOF

#!/usr/bin/env python3
"""Dominion Game Code"""

import json
import random
import sys
from typing import List, Optional, Any
from uuid import UUID

import dominion.game_setup as game_setup
from dominion import NoCardException
from dominion.Artifact import Artifact
from dominion.Boon import Boon
from dominion.Card import Card
from dominion.CardPile import CardPile
from dominion.Event import Event
from dominion.Hex import Hex
from dominion.Landmark import Landmark
from dominion.PlayArea import PlayArea
from dominion.Player import Player
from dominion.Project import Project
from dominion.Prophecy import Prophecy
from dominion.State import State
from dominion.TextPlayer import TextPlayer
from dominion.Trait import Trait
from dominion.Way import Way


###############################################################################
###############################################################################
###############################################################################
class Game:
    """Game class"""

    def __init__(self, **kwargs: Any) -> None:
        self.players: dict[str, Player] = {}
        self._cards: dict[UUID, Card] = {}
        self.card_piles: dict[str, CardPile] = {}
        self.states: dict[str, State] = {}
        self.artifacts: dict[str, Artifact] = {}
        self.projects: dict[str, Project] = {}
        self.events: dict[str, Event] = {}
        self.ways: dict[str, Way] = {}
        self.landmarks: dict[str, Landmark] = {}
        self.boons: list[Boon] = []
        self.traits: dict[str, Trait] = {}
        self.discarded_boons: list[Boon] = []
        self.retained_boons: list[Boon] = []
        self.hexes: list[Hex] = []
        self._turns: list[str] = []
        self.ally = None
        self.discarded_hexes: list[Hex] = []
        self.trash_pile = PlayArea("trash", game=self)
        self.inactive_prophecy: Optional[Prophecy] = None
        self.prophecy: Optional[Prophecy] = None
        self.game_over = False
        self.quiet = False
        self.heirlooms: list[str] = []
        self.current_player: Optional[Player] = None
        self.sun_tokens: int = 0
        self.numplayers = 0
        self.specials: dict[str, Any] = {}  # Special areas for specific card related stuff
        game_setup.parse_args(self, **kwargs)

        self.card_mapping = game_setup.get_available_card_classes(self)
        self._original: dict[str, int | dict[str, dict[str, int]]] = {}
        self.card_instances: dict[str, Card] = {}

    ###########################################################################
    def start_game(self, player_names: Optional[list[str]] = None, plr_class: type[Player] = TextPlayer) -> None:
        game_setup.start_game(self, player_names, plr_class)

    ###########################################################################
    def _save_original(self) -> None:
        """Save original card state for debugging purposes"""
        self._original["count"] = self._count_all_cards()
        self._original["total_cards"] = self.count_cards()

    ###########################################################################
    def remove_sun_token(self) -> int:
        self.sun_tokens -= 1
        if self.sun_tokens <= 0:
            self.reveal_prophecy()
            self.sun_tokens = 0
        return self.sun_tokens

    ###########################################################################
    def reveal_prophecy(self) -> None:
        if self.prophecy is not None:
            return
        self.output(f"Prophecy {self.inactive_prophecy} is now active")
        self.prophecy = self.inactive_prophecy
        assert self.prophecy is not None
        self.prophecy.hook_reveal_prophecy(self)

    ###########################################################################
    def player_list(self) -> list[Player]:
        """List of players"""
        return list(self.players.values())

    ###########################################################################
    def count_cards(self) -> int:
        """Count the number of cards in the game"""
        count = {"trash": self.trash_pile.size()}
        for name, pile in list(self.card_piles.items()):
            count[f"pile_{name}"] = len(pile)
        for plr in self.player_list():
            count[f"player_{plr.name}"] = plr.count_cards()
        total = sum(count.values())
        return total

    ###########################################################################
    def output(self, msg: str) -> None:
        """Send output to all players"""
        if not self.quiet:
            sys.stdout.write(f"ALL: {msg}\n")

    ###########################################################################
    def assign_trait(self, trait: str, card_pile: str) -> None:
        """Assign the trait to the card pile"""
        self.card_piles[card_pile].trait = trait
        self.traits[trait].card_pile = card_pile

    ###########################################################################
    def getPrizes(self) -> list[str]:
        """TODO"""
        return list(self.card_mapping["PrizeCard"].keys())

    ###########################################################################
    def get_card_from_pile(self, pile: str, name: str = "") -> Card:
        """Get and return a card from pile (with name if specified)"""
        assert isinstance(pile, str), f"{pile=} {type(pile)=}"
        assert pile in self.card_piles, f"{pile=} not in {self.card_piles=}"
        card = self.card_piles[pile].remove(name)
        if card is None:
            raise NoCardException
        return card

    ###########################################################################
    def get_card_piles(self) -> list[tuple[str, CardPile]]:
        """Return the card piles in this game
        While Loot is technically a Pile - it isn't for most purposes
        """
        piles = list(self.card_piles.items())
        return [(key, value) for key, value in piles if key not in ("Loot", "Shelters")]

    ###########################################################################
    def getAvailableCards(self, prefix: str = "Card") -> List[str]:
        """TODO"""
        return list(self.card_mapping[prefix].keys())

    ###########################################################################
    def get_action_piles(self, cost: int = 999) -> list[str]:
        """Return all card stacks that are action cards that cost less than cost"""
        action_piles = []
        for name, pile in self.card_piles.items():
            try:
                card = pile.get_top_card()
            except NoCardException:  # pragma: no coverage
                continue
            if not card.purchasable:
                continue
            if card.cost > cost:
                continue
            if card.isAction():
                action_piles.append(name)
        return action_piles

    ###########################################################################
    def get_treasure_piles(self) -> list[str]:
        """Return all card stacks that are treasure cards"""
        treasure_piles = []
        for name, _ in self.get_card_piles():
            card = self.card_instances[name]
            if card.isTreasure():
                treasure_piles.append(name)
        return treasure_piles

    ###########################################################################
    def get_victory_piles(self) -> list[str]:
        """Return all card stack names that are victory cards"""
        victory_piles = []
        for name, _ in self.get_card_piles():
            if name in ("Shelters",):
                continue
            card = self.card_instances[name]
            if card.isVictory():
                victory_piles.append(name)
        return victory_piles

    ###########################################################################
    def isGameOver(self) -> bool:
        """is the game over"""
        empties = []
        for cpile in self.card_piles:
            if self.card_piles[cpile].is_empty():
                empties.append(cpile)
        if len(empties) >= 3:
            self.output(f"Game Over: {', '.join(empties)} piles are empty")
            return True

        if self.card_piles["Province"].is_empty():
            self.output("Game Over: Province pile is empty")
            return True
        return False

    ###########################################################################
    def receive_hex(self) -> Optional[Hex]:
        """Receive a hex"""
        if not self.hexes:
            self.cleanup_hexes()
        hx = self.hexes.pop()
        return hx

    ###########################################################################
    def cleanup_hexes(self) -> None:
        """TODO"""
        for hx in self.discarded_hexes[:]:
            self.hexes.append(hx)
        random.shuffle(self.hexes)
        self.discarded_hexes = []

    ###########################################################################
    def discard_hex(self, hx: Hex) -> None:
        """Return a hex"""
        self.discarded_hexes.append(hx)

    ###########################################################################
    def receive_boon(self) -> Optional[Boon]:
        """Receive a boon"""
        if not self.boons:
            self.boons = self.discarded_boons[:]
            self.discarded_boons = []
            random.shuffle(self.boons)
        try:
            boon = self.boons.pop()
        except IndexError:
            boon = None
        return boon

    ###########################################################################
    def cleanup_boons(self) -> None:
        """TODO"""
        for boon in self.retained_boons[:]:
            self.discarded_boons.append(boon)
        self.retained_boons = []
        for boon in self.discarded_boons[:]:
            self.boons.append(boon)
        random.shuffle(self.boons)
        self.discarded_boons = []

    ###########################################################################
    def discard_boon(self, boon: Boon) -> None:
        """Return a boon"""
        if boon.retain_boon:
            self.retained_boons.append(boon)
        else:
            self.discarded_boons.append(boon)

    ###########################################################################
    def print_state(self, card_dump: bool = False) -> None:  # pragma: no cover
        """This is used for debugging"""
        print("\n" + "#" * 80)
        print(f"Trash: {', '.join([_.name for _ in self.trash_pile])}")
        print(f"Boons: {', '.join([_.name for _ in self.boons])}")
        print(f"Hexes: {', '.join([_.name for _ in self.hexes])}")
        print(f"Prophecy: {self.inactive_prophecy} Tokens: {self.sun_tokens}")
        if self.ally:
            print(f"Ally: {self.ally.name}")
        print(f"Projects: {', '.join([_.name for _ in self.projects.values()])}")
        for name, card_pile in self.card_piles.items():
            tokens = ""
            for plr in self.player_list():
                tkns = plr.which_token(name)
                if tkns:
                    tokens += f"{plr.name}[{','.join(tkns)}]"

            print(f"CardPile {name}: {len(card_pile)} cards {tokens}")
        print(f"Instances: {', '.join([_ for _ in self.card_instances])}")

        for plr in self.player_list():
            plr.print_state()
        print()
        if card_dump:
            for v in self._cards.values():
                print(f"    {v} ({v.uuid} {v._player}@{v._location})")

    ###########################################################################
    def player_to_left(self, plr: Player) -> Player:
        """Return the player to the 'left' of the one specified"""
        players = self.player_list()
        place = players.index(plr) - 1
        return players[place]

    ###########################################################################
    def playerToRight(self, plr: Player) -> Player:
        """Return the player to the 'right' of the one specified"""
        players = self.player_list()
        place = (players.index(plr) + 1) % len(players)
        return players[place]

    ###########################################################################
    def whoWon(self) -> dict[str, int]:
        """TODO"""
        scores: dict[str, int] = {}
        self.output("")
        self.output("Scores:")
        for plr in self.player_list():
            scores[plr.name] = plr.get_score(verbose=True)
        self.output(json.dumps(scores, indent=2))
        self.output("")
        for plr in self.player_list():
            self.output(f"Cards of {plr.name}:")
            for k, v in plr.get_cards().items():
                self.output(f"{plr.name}: {k}={v}")
        return scores

    ###########################################################################
    def last_turn(self, plr: Player) -> bool:
        """Who had the last turn"""
        try:
            return self._turns[-1] == plr.uuid
        except IndexError:
            return False

    ###########################################################################
    def _count_all_cards(self) -> dict[str, dict[str, int]]:  # pragma: no cover
        """Return where all the cards are"""
        tmp: dict[str, dict[str, int]] = {}
        for pile_name, pile in self.card_piles.items():
            tmp[pile_name] = {}
            total = len(pile)
            tmp[pile_name]["pile"] = total
            for plr in self.player_list():
                for stack_name, stack in plr.piles.items():
                    if count := sum(1 for card in stack if card.pile == pile_name):
                        tmp[pile_name][f"{plr.name}:{stack_name}"] = count
                        total += count
            if count := sum(1 for card in self.trash_pile if card.name == pile_name):
                tmp[pile_name]["trash"] = count
                total += count
            tmp[pile_name]["total"] = total
        return tmp

    ###########################################################################
    def _card_loc_debug(self) -> None:  # pragma: no coverage
        """Dump info to help debug card location errors"""
        now = self._count_all_cards()
        print(f"\n{'- -' * 15} Card Loc Debug: {'- -' * 15}", file=sys.stderr)
        print(
            f"current={self.count_cards()} original={self._original['total_cards']}\n",
            file=sys.stderr,
        )
        for name, pile in self.card_piles.items():
            if self._original["count"][name]["total"] == now[name]["total"]:
                continue
            print(f"{name} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", file=sys.stderr)
            print(f" {name} Original:")
            try:
                print(json.dumps(self._original["count"][name], indent=2), file=sys.stderr)
            except KeyError:
                print(f"Unhandled card {name}")
            print(f" {name} Now:")
            print(json.dumps(now[name], indent=2), file=sys.stderr)
        print(f"{'- -' * 20}", file=sys.stderr)
        for plr in self.players.values():
            plr.debug_all_cards()
        print(f"{'- -' * 20}", file=sys.stderr)

    ###########################################################################
    def _validate_cards(self) -> None:  # pragma: no coverage
        try:
            assert self.count_cards() == self._original["total_cards"]
        except AssertionError:
            self._card_loc_debug()
            raise

    ###########################################################################
    def turn(self) -> None:
        """TODO"""
        self._validate_cards()
        self.current_player = self.player_to_left(self.current_player)
        assert self.current_player is not None
        self.current_player.start_turn()
        self.current_player.turn()
        self.current_player.end_turn()
        self._validate_cards()
        self._turns.append(self.current_player.uuid)
        if self.isGameOver():
            self.game_over = True
            for plr in self.player_list():
                plr.game_over()


###############################################################################
class TestGame(Game):
    """Game for testing purposes"""

    def __init__(self, **kwargs: Any) -> None:
        if "allies" not in kwargs:
            kwargs["allies"] = []
            kwargs["ally_path"] = "tests/allies"
        kwargs["shelters"] = False  # Can cause lots of bad interactions
        if "quiet" not in kwargs:
            kwargs["quiet"] = True
        # Shaman causes lots of bad interactions
        if "Shaman" not in kwargs.get("initcards", []):
            kwargs["badcards"] = kwargs.get("badcards", [])
            kwargs["badcards"].append("Shaman")
        super().__init__(**kwargs)


# EOF

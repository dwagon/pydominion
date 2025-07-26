#!/usr/bin/env python3
"""Dominion Game Code"""
# pylint: disable=too-many-arguments, too-many-branches, too-many-instance-attributes, invalid-name

import json
import random
import sys
from typing import List, Optional, Any

import dominion.game_setup as game_setup
from dominion import Keys, NoCardException
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
from dominion.State import State
from dominion.TextPlayer import TextPlayer
from dominion.Trait import Trait
from dominion.Way import Way
from dominion.game_setup import Flags


###############################################################################
###############################################################################
###############################################################################
class Game:  # pylint: disable=too-many-public-methods
    """Game class"""

    def __init__(self, **kwargs: Any) -> None:
        self.players: dict[str, Player] = {}
        self.bot = False
        self.randobot = 0
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
        self.game_over = False
        self.heirlooms: list[str] = []
        self.flags: dict[Flags, bool] = {
            Flags.ALLOW_SHELTERS: True,
            Flags.LOADED_TRAVELLERS: False,
            Flags.LOADED_PRIZES: False,
            Flags.ALLOW_POTIONS: True,
        }
        self.current_player = None
        self.specials: dict[str, Any] = {}  # Special areas for specific card related stuff
        self.paths = {
            Keys.CARDS: "dominion/cards",
            Keys.ALLIES: "dominion/allies",
            Keys.HEXES: "dominion/hexes",
            Keys.BOONS: "dominion/boons",
            Keys.STATES: "dominion/states",
            Keys.ARTIFACTS: "dominion/artifacts",
            Keys.PROJECTS: "dominion/projects",
            Keys.LOOT: "dominion/loot",
            Keys.LANDMARK: "dominion/landmarks",
            Keys.EVENT: "dominion/events",
            Keys.TRAITS: "dominion/traits",
            Keys.WAY: "dominion/ways",
        }
        self.init_numbers = {
            Keys.EVENT: 0,
            Keys.LANDMARK: 0,
            Keys.PROJECTS: 0,
            Keys.TRAITS: 0,
            Keys.WAY: 0,
        }
        self.init: dict[Keys, list[Any]] = {
            Keys.CARDS: [],
            Keys.BAD_CARDS: [],
            Keys.ALLIES: [],
            Keys.EVENT: [],
            Keys.PROJECTS: [],
            Keys.LANDMARK: [],
            Keys.TRAITS: [],
            Keys.WAY: [],
        }
        # The _base_cards are in every game
        self._base_cards = ["Copper", "Silver", "Gold", "Estate", "Duchy", "Province"]
        self.parse_args(**kwargs)
        if self.prosperity:
            self._base_cards.append("Colony")
            self._base_cards.append("Platinum")

        self.card_mapping = game_setup.get_available_card_classes(self)
        self._original: dict[str, int | dict[str, dict[str, int]]] = {}
        self._cards: dict[str, Card] = {}
        self.card_instances: dict[str, Card] = {}

    ###########################################################################
    def parse_args(self, **args: Any) -> None:
        """Parse the arguments passed to the class"""
        self.paths[Keys.CARDS] = args.get("card_path", self.paths[Keys.CARDS])
        self.paths[Keys.ALLIES] = args.get("ally_path", self.paths[Keys.ALLIES])
        self.paths[Keys.HEXES] = args.get("hex_path", self.paths[Keys.HEXES])
        self.paths[Keys.BOONS] = args.get("boon_path", self.paths[Keys.BOONS])
        self.paths[Keys.STATES] = args.get("state_path", self.paths[Keys.STATES])
        self.paths[Keys.ARTIFACTS] = args.get("artifact_path", self.paths[Keys.ARTIFACTS])
        self.paths[Keys.PROJECTS] = args.get("project_path", self.paths[Keys.PROJECTS])
        self.paths[Keys.LANDMARK] = args.get("landmark_path", self.paths[Keys.LANDMARK])
        self.paths[Keys.EVENT] = args.get("event_path", self.paths[Keys.EVENT])
        self.paths[Keys.TRAITS] = args.get("trait_path", self.paths[Keys.TRAITS])
        self.paths[Keys.WAY] = args.get("way_path", self.paths[Keys.WAY])

        self.init_numbers[Keys.EVENT] = args.get("num_events", 0)
        self.init_numbers[Keys.WAY] = args.get("num_ways", 0)
        self.init_numbers[Keys.LANDMARK] = args.get("num_landmarks", 0)
        self.init_numbers[Keys.PROJECTS] = args.get("num_projects", 0)
        self.init_numbers[Keys.TRAITS] = args.get("num_traits", 0)

        self.init[Keys.CARDS] = args.get("initcards", [])
        self.init[Keys.BAD_CARDS] = args.get("badcards", [])
        self.init[Keys.EVENT] = args.get("events", [])
        self.init[Keys.WAY] = args.get("ways", [])
        self.init[Keys.LANDMARK] = args.get("landmarks", [])
        self.init[Keys.PROJECTS] = args.get("projects", [])
        self.init[Keys.ALLIES] = args.get("allies", [])
        self.init[Keys.TRAITS] = args.get("traits", [])

        self.num_stacks = args.get("num_stacks", 10)
        self.flags[Flags.ALLOW_POTIONS] = args.get("potions", True)
        self.prosperity = args.get("prosperity", False)
        self.oldcards = args.get("oldcards", False)
        self.quiet = args.get("quiet", False)
        self.numplayers = args.get("numplayers", 2)
        self.bot = args.get("bot", False)
        self.randobot = args.get("randobot", 0)
        self.flags[Flags.ALLOW_SHELTERS] = args.get("shelters", True)

    ###########################################################################
    def start_game(
        self,
        player_names: Optional[list[str]] = None,
        plr_class: type[Player] = TextPlayer,
    ) -> None:
        """Initialise game bits"""

        game_setup.load_decks(self, self.init[Keys.CARDS], self.num_stacks)
        self.events = game_setup.load_events(self, self.init[Keys.EVENT], self.init_numbers[Keys.EVENT])
        self.ways = game_setup.load_ways(self, self.init[Keys.WAY], self.init_numbers[Keys.WAY])
        self.landmarks = game_setup.load_landmarks(self, self.init[Keys.LANDMARK], self.init_numbers[Keys.LANDMARK])
        game_setup.load_artifacts(self)
        game_setup.load_projects(self, self.init[Keys.PROJECTS], self.init_numbers[Keys.PROJECTS])
        game_setup.load_traits(self, self.init[Keys.TRAITS], self.init_numbers[Keys.TRAITS])

        if self.hexes or self.boons:
            game_setup.load_states(self)
        game_setup.check_card_requirements(self)
        game_setup.setup_players(self, player_names, plr_class)
        self.card_setup()  # Has to be after players have been created
        game_setup.check_card_requirements(self)  # Again as setup can add requirements
        self.current_player = self.player_list()[0]
        if self.ally:
            for plr in self.player_list():
                plr.favors.add(1)
        self._save_original()

    ###########################################################################
    def _save_original(self) -> None:
        """Save original card state for debugging purposes"""
        self._original["count"] = self._count_all_cards()
        self._original["total_cards"] = self.count_cards()

    ###########################################################################
    def player_list(self) -> list[Player]:
        """List of players"""
        return list(self.players.values())

    ###########################################################################
    def card_setup(self) -> None:
        """Run the setup() method for all cards"""
        for name, card_pile in list(self.card_piles.items()):
            card_pile.setup(game=self)
        for landmark in list(self.landmarks.values()):
            landmark.setup(game=self)

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
    def __contains__(self, key: str) -> bool:
        """TODO"""
        return key in self.card_piles

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
            except NoCardException:
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
    def _card_loc_debug(self) -> None:
        """Dump info to help debug card location errors"""
        now = self._count_all_cards()
        print(f"{'- -' * 20}", file=sys.stderr)
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
    def _validate_cards(self) -> None:
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

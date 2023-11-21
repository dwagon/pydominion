#!/usr/bin/env python3
""" Dominion Game Code """
# pylint: disable=too-many-arguments, too-many-branches, too-many-instance-attributes, invalid-name
import glob
import json
import importlib
import os
import random
import sys
import uuid
from typing import List, Optional, Any, Callable

from dominion import Piles, Keys, NoCardException
from dominion.Boon import Boon, BoonPile
from dominion.Loot import LootPile
from dominion.BotPlayer import BotPlayer
from dominion.RandobotPlayer import RandobotPlayer
from dominion.Card import Card, CardExpansion
from dominion.CardPile import CardPile
from dominion.Hex import Hex, HexPile
from dominion.Names import playerNames
from dominion.PlayArea import PlayArea
from dominion.Player import Player
from dominion.TextPlayer import TextPlayer
from dominion.State import State
from dominion.Artifact import Artifact
from dominion.Project import Project
from dominion.Event import Event
from dominion.Way import Way
from dominion.Landmark import Landmark
from dominion.Trait import Trait


###############################################################################
###############################################################################
###############################################################################
class Game:  # pylint: disable=too-many-public-methods
    """Game class"""

    def __init__(self, **kwargs: Any) -> None:
        self.players: dict[str, Player] = {}
        self.bot = False
        self.randobot = False
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
        self._heirlooms: list[str] = []
        self._allow_shelters = True
        self._loaded_prizes = False
        self._allow_potions = True
        self.current_player = None
        self.specials: dict[
            str, Any
        ] = {}  # Special areas for specific card related stuff
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

        self.card_mapping = self._get_available_card_classes()
        self._original = {}
        self.loaded_travellers = False  # For testing purposes
        self._cards = {}
        self.card_instances: dict[str, Card] = {}

    ###########################################################################
    def parse_args(self, **args: Any) -> None:
        """Parse the arguments passed to the class"""
        self.paths[Keys.CARDS] = args.get("card_path", self.paths[Keys.CARDS])
        self.paths[Keys.ALLIES] = args.get("ally_path", self.paths[Keys.ALLIES])
        self.paths[Keys.HEXES] = args.get("hex_path", self.paths[Keys.HEXES])
        self.paths[Keys.BOONS] = args.get("boon_path", self.paths[Keys.BOONS])
        self.paths[Keys.STATES] = args.get("state_path", self.paths[Keys.STATES])
        self.paths[Keys.ARTIFACTS] = args.get(
            "artifact_path", self.paths[Keys.ARTIFACTS]
        )
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
        self._allow_potions = args.get("potions", True)
        self.prosperity = args.get("prosperity", False)
        self.oldcards = args.get("oldcards", False)
        self.quiet = args.get("quiet", False)
        self.numplayers = args.get("numplayers", 2)
        self.bot = args.get("bot", False)
        self.randobot = args.get("randobot", 0)
        self._allow_shelters = args.get("shelters", True)

    ###########################################################################
    def _use_shelters(self) -> bool:
        """Should we use shelters"""
        use_shelters = False

        if "shelters" in [_.lower() for _ in self.init[Keys.CARDS]]:
            use_shelters = True
        elif not self._allow_shelters:
            return False

        # Pick a card to see if it is a dark ages card
        halfway = len(self.card_piles) // 2
        name, card_pile = list(self.card_piles.items())[halfway]
        card = self.card_instances[name]
        if card.base == CardExpansion.DARKAGES:
            use_shelters = True

        if use_shelters:
            self.card_piles["Shelters"] = CardPile(self)
            for _ in range(self.numplayers):
                shelters = ["Overgrown Estate", "Hovel", "Necropolis"]
                for shelter in shelters:
                    self.card_instances[shelter] = self.card_mapping["Shelter"][
                        shelter
                    ]()
                    shelter_card = self.card_mapping["Shelter"][shelter]()
                    self.card_piles["Shelters"].add(shelter_card)
        return use_shelters

    ###########################################################################
    def start_game(
        self, player_names: Optional[list[str]] = None, plr_class=TextPlayer
    ) -> None:
        """Initialise game bits"""

        self._load_decks(self.init[Keys.CARDS], self.num_stacks)
        self._load_events()
        self._load_ways()
        self._load_landmarks()
        self._load_artifacts()
        self._load_projects()
        self._load_traits()

        if self.hexes or self.boons:
            self._load_states()
        self._check_card_requirements()
        self._setup_players(player_names, plr_class)
        self.card_setup()  # Has to be after players have been created
        self.current_player = self.player_list()[0]
        if self.ally:
            for plr in self.player_list():
                plr.favors.add(1)
        self._save_original()

    ###########################################################################
    def _setup_players(
        self, playernames: Optional[list[str]] = None, plr_class: Callable = TextPlayer
    ) -> None:
        use_shelters = self._use_shelters()
        names = playerNames[:]
        if playernames is None:
            playernames = []

        for player_num in range(self.numplayers):
            try:
                name = playernames.pop()
            except IndexError:
                name = random.choice(names)
                names.remove(name)
            the_uuid = uuid.uuid4().hex
            if self.bot:
                self.players[the_uuid] = BotPlayer(
                    game=self,
                    quiet=self.quiet,
                    name=f"{name}Bot",
                    heirlooms=self._heirlooms,
                    use_shelters=use_shelters,
                )
                self.bot = False
            elif self.randobot:
                self.players[the_uuid] = RandobotPlayer(
                    game=self,
                    quiet=self.quiet,
                    name=f"{name}RandoBot",
                    heirlooms=self._heirlooms,
                    use_shelters=use_shelters,
                )
                self.randobot -= 1
            else:
                self.players[the_uuid] = plr_class(
                    game=self,
                    quiet=self.quiet,
                    name=name,
                    number=player_num,
                    heirlooms=self._heirlooms,
                    use_shelters=use_shelters,
                )
            self.players[the_uuid].uuid = the_uuid

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
            try:  # Handle empty card piles
                card_pile.setup(game=self)
            except TypeError:
                pass
        for landmark in list(self.landmarks.values()):
            landmark.setup(game=self)

    ###########################################################################
    def count_cards(self) -> int:
        """TODO"""
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
    def _load_travellers(self) -> None:
        """TODO"""
        travellers = self.getAvailableCards("Traveller")
        for trav in travellers:
            self._use_card_pile(None, trav, True, "Traveller")
        self.loaded_travellers = True

    ############################################################################
    def _load_loot(self) -> None:
        """Load Loot cards into game"""
        if "Loot" in self.card_piles:
            return
        self.output("Using Loot cards")
        self.card_piles["Loot"] = LootPile(self)
        self.card_piles["Loot"].init_cards()

    ###########################################################################
    def _load_ways(self) -> None:
        """Load required Ways"""
        way_cards = []
        for wname in self.init[Keys.WAY]:
            if not wname.lower().startswith("way of the "):
                way_cards.append(f"Way of the {wname}")
            else:
                way_cards.append(wname)
        self.ways = self._load_non_kingdom_cards(
            cardtype="Way",
            specified=way_cards,
            num_required=self.init_numbers[Keys.WAY],
        )
        if self.ways:
            self.output(f"Playing with {self.ways}")

    ###########################################################################
    def _load_traits(self) -> None:
        """Load required Traits"""
        self.traits = self._load_non_kingdom_cards(
            cardtype="Trait",
            specified=self.init[Keys.TRAITS],
            num_required=self.init_numbers[Keys.TRAITS],
        )
        for trait in self.traits:
            card_piles = []
            for pile in self.card_piles:
                if self.card_piles[pile].trait:
                    continue
                if pile in self._base_cards:
                    continue
                if pile in ("Loot",):
                    continue
                card = self.card_instances[pile]
                if not card.purchasable:
                    continue
                if not card.isAction() and not card.isTreasure():
                    continue
                card_piles.append(pile)
            card_pile = random.choice(card_piles)
            self.assign_trait(trait, card_pile)

    ###########################################################################
    def assign_trait(self, trait: str, card_pile: str) -> None:
        """Assign the trait to the card pile"""
        self.card_piles[card_pile].trait = trait
        self.traits[trait].card_pile = card_pile

    ###########################################################################
    def _load_events(self) -> None:
        """Load required events"""
        self.events = self._load_non_kingdom_cards(
            cardtype="Event",
            specified=self.init[Keys.EVENT],
            num_required=self.init_numbers[Keys.EVENT],
        )
        if self.events:
            self.output(
                f"Playing with Events: {', '.join(event for event in self.events)}"
            )

    ###########################################################################
    def _load_landmarks(self) -> None:
        """Load required landmarks"""
        self.landmarks = self._load_non_kingdom_cards(
            "Landmark",
            self.init[Keys.LANDMARK],
            self.init_numbers[Keys.LANDMARK],
        )
        if self.landmarks:
            self.output(f"Playing with Landmarks {self.landmarks}")

    ###########################################################################
    def _load_boons(self) -> None:
        """Load boons into Pile"""
        if self.boons:
            return
        self.output("Using boons")
        d = self._load_non_kingdom_pile("Boon", BoonPile)
        self.boons = list(d.values())
        random.shuffle(self.boons)

    ###########################################################################
    def _load_hexes(self) -> None:
        """Load Hexes into Pile"""
        if self.hexes:
            return
        self.output("Using hexes")
        d = self._load_non_kingdom_pile("Hex", HexPile)
        self.hexes = list(d.values())
        random.shuffle(self.hexes)

    ###########################################################################
    def _load_states(self) -> None:
        """TODO"""
        if self.states:
            return
        self.output("Using states")
        self.states = self._load_non_kingdom_cards("State", None, None)

    ###########################################################################
    def _load_artifacts(self) -> None:
        """TODO"""
        if self.artifacts:
            return
        self.artifacts = self._load_non_kingdom_cards("Artifact", None, None)
        self.output("Playing with Artifacts")

    ###########################################################################
    def _load_projects(self) -> None:
        """TODO"""
        if self.projects:
            return
        self.projects = self._load_non_kingdom_cards(
            "Project",
            self.init[Keys.PROJECTS],
            self.init_numbers[Keys.PROJECTS],
        )
        if self.projects:
            self.output(f"Playing with Project {self.projects}")

    ###########################################################################
    def _load_ally(self) -> None:
        """Load the ally"""
        if isinstance(self.init[Keys.ALLIES], str):
            self.init[Keys.ALLIES] = [self.init[Keys.ALLIES]]
        allies = self._load_non_kingdom_cards("Ally", self.init[Keys.ALLIES], 1)
        self.ally = list(allies.values())[0]
        self.output(f"Playing with Ally {self.ally}")

    ###########################################################################
    def good_names(self, specified: list[str], cardtype: str) -> list[str]:
        """Replace specified names with ones that are good"""
        answer: list[str] = []
        for name in specified:
            if name in self.card_mapping[cardtype]:
                answer.append(name)
            else:
                good_name = self.guess_card_name(name, cardtype)
                if good_name is None:
                    sys.stderr.write(f"Unknown {cardtype} '{name}'\n")
                    sys.exit(1)
                answer.append(good_name)
        return answer

    ###########################################################################
    def _load_non_kingdom_pile(self, cardtype: str, pileClass) -> dict[str, CardPile]:
        """Load non kingdom cards into a pile
        Returns a dictionary; key is the name, value is the instance
        """
        dest: dict[str, CardPile] = {}
        available = self.getAvailableCards(cardtype)
        # To make up the numbers
        for nkc in available:
            klass = self.card_mapping[cardtype][nkc]
            dest[nkc] = pileClass(nkc, klass)
        return dest

    ###########################################################################
    def instantiate_non_kingdom_card(self, cardtype: str, card_name: str) -> Card:
        klass = self.card_mapping[cardtype][card_name]
        return klass()

    ###########################################################################
    def _load_non_kingdom_cards(
        self, cardtype: str, specified, num_required: Optional[int] = None
    ):
        """Load non kingdom cards into the game
        If specific cards are required they need to be in `specified`
        Up to numrequired cards will be used

        Returns a dictionary; key is the name, value is the instance
        """
        dest = {}
        available = self.getAvailableCards(cardtype)
        # Specified cards
        if specified is not None:
            names = self.good_names(specified, cardtype)
            for nkc in names:
                dest[nkc] = self.instantiate_non_kingdom_card(cardtype, nkc)
                available.remove(nkc)

        # To make up the numbers
        if num_required is not None:
            while len(dest) < num_required:
                nkc = random.choice(available)
                dest[nkc] = self.instantiate_non_kingdom_card(cardtype, nkc)
                available.remove(nkc)
        else:  # Do them all
            for nkc in available:
                dest[nkc] = self.instantiate_non_kingdom_card(cardtype, nkc)

        return dest

    ###########################################################################
    def guess_card_name(self, name: str, prefix: str = "Card") -> Optional[str]:
        """Don't force the user to give the exact card name on the command
        line - maybe we can guess it"""
        available = self.getAvailableCards(prefix)
        if name in available:
            return name
        for card_name in available:
            newc = card_name.replace("'", "")
            if newc.lower() == name.lower():
                return card_name
            newc = newc.replace(" ", "")
            if newc.lower() == name.lower():
                return card_name
            newc = newc.replace(" ", "_")
            if newc.lower() == name.lower():
                return card_name
            newc = newc.replace(" ", "-")
            if newc.lower() == name.lower():
                return card_name
            name = name.replace("_", "")
            if newc.lower() == name.lower():
                return card_name
        return None

    ###########################################################################
    def _place_init_card(self, card: str, available: list[str]) -> Optional[int]:
        """For the specified card, load it into the correct deck
        Return the number of kingdom card piles used or None for not found
        """
        # If base cards are specified by initcards
        if card_name := self.guess_card_name(card, prefix="BaseCard"):
            self._use_card_pile(None, card_name, force=True, card_type="BaseCard")
        elif card_name := self.guess_card_name(card):
            return self._use_card_pile(available, card_name, force=True)
        elif event_name := self.guess_card_name(card, "Event"):
            self.init[Keys.EVENT].append(event_name)
        elif way_name := self.guess_card_name(card, "Way"):
            self.init[Keys.WAY].append(way_name)
        elif landmark_name := self.guess_card_name(card, "Landmark"):
            self.init[Keys.LANDMARK].append(landmark_name)
        elif project_name := self.guess_card_name(card, "Project"):
            self.init[Keys.PROJECTS].append(project_name)
        elif ally_name := self.guess_card_name(card, "Ally"):
            self.init[Keys.ALLIES].append(ally_name)
        elif trait_name := self.guess_card_name(card, "Trait"):
            self.init[Keys.TRAITS].append(trait_name)
        elif self.guess_card_name(card, "Boon"):
            self._load_boons()
        elif self.guess_card_name(card, "Artifact"):
            # Artifacts should be loaded by the requiring card but can still be specified
            # in a card set
            pass
        elif card.lower() == "shelters":
            # Use of shelters handled elsewhere
            pass
        else:
            print(f"Can't guess what card '{card}' is")
            return None
        return 0

    ###########################################################################
    def _load_decks(self, initcards: list[str], numstacks: int) -> None:
        """Determine what cards we are using this game"""
        for card in self._base_cards:
            self._use_card_pile(
                self._base_cards[:], card, force=True, card_type="BaseCard"
            )
        available = self.getAvailableCards()
        unfilled = numstacks
        found_all = True
        for crd in initcards:
            # These cards get loaded by other things
            if crd in ("Boons", "Hexes"):
                continue
            result = self._place_init_card(crd, available)
            if result is None:
                found_all = False
            else:
                unfilled -= result

        if not found_all:
            sys.exit(1)

        while unfilled > 0:
            if not available:
                # Not enough cards to fill the hand - almost certainly in a test
                break
            crd = random.choice(available)
            if crd in self.init[Keys.BAD_CARDS]:
                continue
            unfilled -= self._use_card_pile(available, crd)

        self._check_card_requirements()

    ###########################################################################
    def _add_prizes(self) -> None:
        """TODO"""
        for prize in self.getAvailableCards("PrizeCard"):
            self._use_card_pile(None, prize, False, "PrizeCard")
        self._loaded_prizes = True

    ###########################################################################
    def getPrizes(self) -> list[str]:
        """TODO"""
        return list(self.card_mapping["PrizeCard"].keys())

    ###########################################################################
    def _num_cards_in_pile(self, card: Card) -> int:
        """Return the number of cards that should be in a card pile"""
        if hasattr(card, "calc_numcards"):
            num_cards = card.calc_numcards(self)
        elif hasattr(card, "numcards"):
            num_cards = card.numcards
        else:
            num_cards = 10
        return num_cards

    ###########################################################################
    def _use_card_pile(
        self, available, card_name: str, force=False, card_type="Card"
    ) -> int:
        """Set up a card pile for use
        Return 1 if it counts against the number of card piles in use"""
        try:
            if available is not None:
                available.remove(card_name)
        except ValueError:  # pragma: no cover
            print(f"Unknown card '{card_name}'\n", file=sys.stderr)
            sys.exit(1)
        card = self.card_mapping[card_type][card_name]()
        if not self._allow_potions and card.potcost:
            return 0
        if hasattr(card, "cardpile_setup"):
            card_pile = card.cardpile_setup(self)
        else:
            card_pile = CardPile(self)
        num_cards = self._num_cards_in_pile(card)
        card_pile.init_cards(num_cards, self.card_mapping[card_type][card_name])
        if not force and not card.insupply:
            return 0

        self.card_piles[card_name] = card_pile
        for card in card_pile:
            if card_name not in self.card_instances:
                self.card_instances[card_name] = self.card_mapping[card_type][
                    card_name
                ]()
            self._cards[card.uuid] = card
            if not card.pile:
                card.pile = card_name
            card.location = Piles.CARDPILE
        self.output(f"Playing with {card_name}")
        return 1

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
    def _use_ruins(self, card: Card) -> None:
        """Use Ruins"""
        self.output(f"Playing with Ruins as required by {card}")
        self._use_card_pile(None, "Ruins", True)

    ###########################################################################
    def check_card_requirement(self, card: Card) -> None:
        for x in card.required_cards:
            card_type = "Card"
            if x == "Loot":
                self._load_loot()
                continue
            if isinstance(x, tuple):
                card_type, card_name = x
            else:
                card_type, card_name = "BaseCard", x
            if card_name not in self.card_piles:
                self._use_card_pile(None, card_name, force=True, card_type=card_type)
                self.output(f"Playing with {card_name} as required by {card}")

        if card.heirloom is not None and card.heirloom not in self._heirlooms:
            self._use_card_pile(None, card.heirloom, force=True, card_type="Heirloom")
            self._heirlooms.append(card.heirloom)
            self.output(f"Playing with {card.heirloom} as required by {card}")

        if card.isLooter() and "Ruins" not in self.card_piles:
            self._use_ruins(card)
        if card.isFate() and not self.boons:
            self._load_boons()
        if card.isDoom() and not self.hexes:
            self._load_hexes()
            self.output(f"Using hexes as required by {card}")
        if card.isLiaison() and not self.ally:
            self._load_ally()
            self.output(f"Using Allies as required by {card}")
        if card.traveller and not self.loaded_travellers:
            self._load_travellers()
        if card.needs_prizes and not self._loaded_prizes:
            self._add_prizes()
            self.output(f"Playing with Prizes as required by {card}")
        if card.needsartifacts and not self.artifacts:
            self._load_artifacts()
            self.output(f"Using artifacts as required by {card}")
        if card.needsprojects and not self.projects:
            self._load_projects()
            self.output(f"Using projects as required by {card}")

    ###########################################################################
    def _check_card_requirements(self) -> None:
        """If any card we are playing requires another card (e.g. Curse) then
        ensure that is loaded as well"""

        check_cards = (
            list(self._cards.values())
            + list(self.events.values())
            + list(self.traits.values())
            + list(self.hexes)
            + list(self.boons)
            + list(self.landmarks.values())
        )
        if self.ally:
            check_cards.append(self.ally)

        for card in check_cards:
            self.check_card_requirement(card)

        if self.init[Keys.ALLIES] and not self.ally:
            print(
                f"Need to specify a Liaison as well as an Ally {self.init[Keys.ALLIES]}"
            )
            sys.exit(1)

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
    def _get_available_card_classes(self) -> dict[str, dict[str, type[Card]]]:
        """Create a mapping between the card name and the module of that card"""
        mapping: dict[str, dict[str, type[Card]]] = {}
        for prefix in (
            "Card",
            "BaseCard",
            "Traveller",
            "PrizeCard",
            "Castle",
            "Heirloom",
            "Shelter",
            "Split",
        ):
            mapping[prefix] = self.get_card_classes(
                prefix, self.paths[Keys.CARDS], "Card_"
            )
            if self.oldcards:
                old_path = os.path.join(self.paths[Keys.CARDS], "old")
                mapping[prefix].update(self.get_card_classes(prefix, old_path, "Card_"))
        mapping["Event"] = self.get_card_classes(
            "Event", self.paths[Keys.EVENT], "Event_"
        )
        mapping["Way"] = self.get_card_classes("Way", self.paths[Keys.WAY], "Way_")
        mapping["Landmark"] = self.get_card_classes(
            "Landmark", self.paths[Keys.LANDMARK], "Landmark_"
        )
        mapping["Boon"] = self.get_card_classes("Boon", self.paths[Keys.BOONS], "Boon_")
        mapping["Hex"] = self.get_card_classes("Hex", self.paths[Keys.HEXES], "Hex_")
        mapping["State"] = self.get_card_classes(
            "State", self.paths[Keys.STATES], "State_"
        )
        mapping["Artifact"] = self.get_card_classes(
            "Artifact", self.paths[Keys.ARTIFACTS], "Artifact_"
        )
        mapping["Project"] = self.get_card_classes(
            "Project", self.paths[Keys.PROJECTS], "Project_"
        )
        mapping["Ally"] = self.get_card_classes(
            "Ally", self.paths[Keys.ALLIES], "Ally_"
        )
        mapping["Trait"] = self.get_card_classes(
            "Trait", self.paths[Keys.TRAITS], "Trait_"
        )
        mapping["Loot"] = self.get_card_classes("Loot", self.paths[Keys.LOOT], "Loot_")
        return mapping

    ###########################################################################
    @classmethod
    def get_card_classes(
        cls, prefix: str, path: str, class_prefix: str = "Card_"
    ) -> dict[str, type[Card]]:
        """Import all the modules to determine the real name of the card
        This is slow, but it is the only way that I can think of

        Look in {path} for files starting with {prefix}
        """
        mapping: dict[str, type[Card]] = {}
        files = glob.glob(f"{path}/{prefix}_*.py")
        for file_name in [os.path.basename(_) for _ in files]:
            file_name = file_name.replace(".py", "")
            mod = importlib.import_module(f"{path.replace('/', '.')}.{file_name}")

            # Find the class in the module that is the one we want (e.g. Card_Foo)
            classes = dir(mod)
            for kls in classes:
                if kls.startswith(class_prefix):
                    klass = getattr(mod, kls)
                    break
            else:  # pragma: no cover
                raise ImportError(f"Couldn't find {prefix} class in {path}\n")
            mapping[klass().name] = klass
            klass().check()
        return mapping

    ###########################################################################
    def getAvailableCards(self, prefix: str = "Card") -> List[str]:
        """TODO"""
        return list(self.card_mapping[prefix].keys())

    ###########################################################################
    def get_action_piles(self, cost=999) -> list[str]:
        """Return all card stacks that are action cards that cost less than cost"""
        action_piles = []
        for name, pile in self.card_piles.items():
            card = pile.get_top_card()
            if not card:
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
    def print_state(self, card_dump=False) -> None:  # pragma: no cover
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
                print(
                    json.dumps(self._original["count"][name], indent=2), file=sys.stderr
                )
            except KeyError:
                print(f"Unhandled card {name}")
            print(f" {name} Now:")
            print(json.dumps(now[name], indent=2), file=sys.stderr)
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

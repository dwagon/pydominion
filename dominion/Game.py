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
from typing import List, Optional

from dominion.Ally import AllyPile
from dominion.ArtifactPile import ArtifactPile
from dominion.BoonPile import BoonPile
from dominion.BotPlayer import BotPlayer
from dominion.RandobotPlayer import RandobotPlayer
from dominion.Card import CardExpansion
from dominion.CardPile import CardPile
from dominion.Event import EventPile
from dominion.HexPile import HexPile
from dominion.LandmarkPile import LandmarkPile
from dominion.Names import playerNames
from dominion.PlayArea import PlayArea
from dominion.Player import Player
from dominion.ProjectPile import ProjectPile
from dominion.RuinCardPile import RuinCardPile
from dominion.StatePile import StatePile
from dominion.TextPlayer import TextPlayer
from dominion.WayPile import WayPile


###############################################################################
###############################################################################
###############################################################################
class Game:  # pylint: disable=too-many-public-methods
    """Game class"""

    def __init__(self, **kwargs):
        self.players = {}
        self.bot = False
        self.randobot = False
        self.cardpiles = {}
        self.states = {}
        self.artifacts = {}
        self.projects = {}
        self.events = {}
        self.ways = {}
        self.landmarks = {}
        self.init_ally = []
        self._init_cardset = set()
        self.boons = []
        self.discarded_boons = []
        self.retained_boons = []
        self.hexes = []
        self._turns = []
        self.ally = None
        self.discarded_hexes = []
        self.trashpile = PlayArea("trash", game=self)
        self.gameover = False
        self._heirlooms = []
        self._allow_shelters = True
        self.current_player = None
        self.paths = {
            "cards": "dominion/cards",
            "allies": "dominion/allies",
            "hexes": "dominion/hexes",
            "boons": "dominion/boons",
            "states": "dominion/states",
            "artifacts": "dominion/artifacts",
            "projects": "dominion/projects",
            "landmarks": "dominion/landmarks",
            "events": "dominion/events",
            "ways": "dominion/ways",
        }
        # The _base_cards are in every game
        self._base_cards = ["Copper", "Silver", "Gold", "Estate", "Duchy", "Province"]
        self.parse_args(**kwargs)
        if self.prosperity:
            self._base_cards.append("Colony")
            self._base_cards.append("Platinum")

        self.cardmapping = self._get_available_card_classes()
        self._total_cards = 0
        self._original = {}
        self.loaded_travellers = False  # For testing purposes
        self._cards = {}

    ###########################################################################
    def parse_args(self, **args):
        """Parse the arguments passed to the class"""
        self.paths["cards"] = args.get("cardpath", self.paths["cards"])
        self.paths["allies"] = args.get("allypath", self.paths["allies"])
        self.paths["hexes"] = args.get("hexpath", self.paths["hexes"])
        self.paths["boons"] = args.get("boonpath", self.paths["boons"])
        self.paths["states"] = args.get("statepath", self.paths["states"])
        self.paths["artifacts"] = args.get("artifactpath", self.paths["artifacts"])
        self.paths["projects"] = args.get("projectpath", self.paths["projects"])
        self.paths["landmarks"] = args.get("landmarkpath", self.paths["landmarks"])
        self.paths["events"] = args.get("eventpath", self.paths["events"])
        self.paths["ways"] = args.get("waypath", self.paths["ways"])

        self.numstacks = args.get("numstacks", 10)
        self.prosperity = args.get("prosperity", False)
        self.oldcards = args.get("oldcards", False)
        self.quiet = args["quiet"] if "quiet" in args else False
        self.numplayers = args["numplayers"] if "numplayers" in args else 2
        self._initcards = args.get("initcards", [])
        self.badcards = args.get("badcards", [])
        self.cardbase = args["cardbase"] if "cardbase" in args else []
        self.bot = args["bot"] if "bot" in args else False
        self.randobot = args.get("randobot", 0)
        self.eventcards = args["eventcards"] if "eventcards" in args else []
        self.waycards = args["waycards"] if "waycards" in args else []
        self.numevents = args["numevents"] if "numevents" in args else 0
        self.numways = args.get("numways", 0)
        self.landmarkcards = args.get("landmarkcards", [])
        self.numlandmarks = args["numlandmarks"] if "numlandmarks" in args else 0
        self.numprojects = args["numprojects"] if "numprojects" in args else 0
        self.initprojects = args["initprojects"] if "initprojects" in args else []
        self.init_ally = args.get("init_ally", args.get("ally", []))
        self._allow_shelters = args.get("shelters", True)

    ###########################################################################
    def _use_shelters(self):
        """Should we use shelters"""
        use_shelters = False

        if "shelters" in [_.lower() for _ in self._initcards]:
            use_shelters = True
        elif not self._allow_shelters:
            return False

        # Pick a card to see if it is a darkages
        halfway = int(len(self.cardpiles) / 2)
        card = list(self.cardpiles.values())[halfway]
        if card.base == CardExpansion.DARKAGES:
            use_shelters = True

        if use_shelters:
            shelters = ["Overgrown Estate", "Hovel", "Necropolis"]
            for crd in shelters:
                cpile = CardPile(crd, self.cardmapping["Shelter"][crd], self)
                self.cardpiles[cpile.name] = cpile
        return use_shelters

    ###########################################################################
    def start_game(self, playernames=None, plrKlass=TextPlayer):
        """Initialise game bits"""
        if playernames is None:
            playernames = []
        names = playerNames[:]
        self._load_decks(self._initcards, self.numstacks)
        self._load_events()
        self._load_ways()
        self._load_landmarks()
        self._load_artifacts()
        self._load_projects()

        if self.hexes or self.boons:
            self._load_states()
        self._check_card_requirements()
        use_shelters = self._use_shelters()

        for plrnum in range(self.numplayers):
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
                self.players[the_uuid] = plrKlass(
                    game=self,
                    quiet=self.quiet,
                    name=name,
                    number=plrnum,
                    heirlooms=self._heirlooms,
                    use_shelters=use_shelters,
                )
            self.players[the_uuid].uuid = the_uuid
        self.card_setup()
        self.current_player = self.player_list(0)
        if self.ally:
            for plr in self.player_list():
                plr.favors.add(1)
        self._save_original()

    ###########################################################################
    def _save_original(self):
        """Save original card state for debugging purposes"""
        self._init_cardset = set(self._cards.keys())
        self._total_cards = self.count_cards()
        self._original = self._count_all_cards()

    ###########################################################################
    def player_list(self, num=None):
        """TODO"""
        if num is None:
            return list(self.players.values())
        return list(self.players.values())[num]

    ###########################################################################
    def card_setup(self):
        """Run the setup() method for all cards"""
        for cpile in list(self.cardpiles.values()):
            cpile.setup(game=self)
        for lmk in list(self.landmarks.values()):
            lmk.setup(game=self)

    ###########################################################################
    def count_cards(self):
        """TODO"""
        count = {}
        count["trash"] = self.trashpile.size()
        for cpile in list(self.cardpiles.values()):
            count[f"pile_{cpile.name}"] = len(cpile)
        for plr in self.player_list():
            count[f"player_{plr.name}"] = plr.count_cards()
        total = sum(count.values())
        return total

    ###########################################################################
    def output(self, msg):
        """Send output to all players"""
        if not self.quiet:
            sys.stdout.write(f"ALL: {msg}\n")

    ###########################################################################
    def _load_travellers(self):
        """TODO"""
        travellers = self.getAvailableCards("Traveller")
        for trav in travellers:
            cpile = CardPile(trav, self.cardmapping["Traveller"][trav], self)
            self.cardpiles[cpile.name] = cpile
        self.loaded_travellers = True

    ###########################################################################
    def _load_ways(self):
        """TODO"""
        waycards = []
        for wname in self.waycards:
            if not wname.lower().startswith("way of the "):
                waycards.append(f"Way of the {wname}")
            else:
                waycards.append(wname)
        self.ways = self._load_non_kingdom_cards(
            cardtype="Way",
            specified=waycards,
            numrequired=self.numways,
            cardKlass=WayPile,
        )

    ###########################################################################
    def _load_events(self):
        """TODO"""
        self.events = self._load_non_kingdom_cards(
            cardtype="Event",
            specified=self.eventcards,
            numrequired=self.numevents,
            cardKlass=EventPile,
        )

    ###########################################################################
    def _load_landmarks(self):
        """TODO"""
        self.landmarks = self._load_non_kingdom_cards("Landmark", self.landmarkcards, self.numlandmarks, LandmarkPile)

    ###########################################################################
    def _load_boons(self):
        """TODO"""
        if self.boons:
            return
        self.output("Using boons")
        d = self._load_non_kingdom_cards("Boon", None, None, BoonPile)
        self.boons = list(d.values())
        random.shuffle(self.boons)

    ###########################################################################
    def _load_hexes(self):
        """TODO"""
        if self.hexes:
            return
        d = self._load_non_kingdom_cards("Hex", None, None, HexPile)
        self.hexes = list(d.values())
        random.shuffle(self.hexes)

    ###########################################################################
    def _load_states(self):
        """TODO"""
        if self.states:
            return
        self.output("Using states")
        self.states = self._load_non_kingdom_cards("State", None, None, StatePile)

    ###########################################################################
    def _load_artifacts(self):
        """TODO"""
        if self.artifacts:
            return
        self.artifacts = self._load_non_kingdom_cards("Artifact", None, None, ArtifactPile)

    ###########################################################################
    def _load_projects(self):
        """TODO"""
        if self.projects:
            return
        self.projects = self._load_non_kingdom_cards("Project", self.initprojects, self.numprojects, ProjectPile)

    ###########################################################################
    def _load_ally(self):
        """Load the allies and pick a single one to have in the game"""
        if isinstance(self.init_ally, str):
            self.init_ally = [self.init_ally]
        allies = self._load_non_kingdom_cards("Ally", self.init_ally, 1, AllyPile)
        self.ally = random.choice(list(allies.values())).ally

    ###########################################################################
    def _load_non_kingdom_cards(self, cardtype, specified, numrequired, cardKlass):
        """Load non kingdom cards into the game
        If specific cards are required they need to be in `specified`
        Up to numrequired cards will be used

        Returns a dictionary; key is the name, value is the instance
        """
        dest = {}
        available = self.getAvailableCards(cardtype)
        # Specified cards
        if specified is not None:
            for nkc in specified:
                try:
                    if nkc not in self.cardmapping[cardtype]:
                        nkc = self.guess_cardname(nkc, cardtype)
                        if nkc is None:
                            sys.stderr.write(f"Unknown {cardtype} '{nkc}'\n")
                            sys.exit(1)
                        print(f"Guessed {nkc}")
                    klass = self.cardmapping[cardtype][nkc]
                    dest[nkc] = cardKlass(nkc, klass)
                    available.remove(nkc)
                except (ValueError, KeyError):
                    sys.stderr.write(f"Unknown {cardtype} '{nkc}'\n")
                    sys.exit(1)
        if numrequired is not None:
            # To make up the numbers
            while len(dest) < numrequired:
                nkc = random.choice(available)
                klass = self.cardmapping[cardtype][nkc]
                dest[nkc] = cardKlass(nkc, klass)
                available.remove(nkc)
        else:  # Do them all
            for nkc in available:
                klass = self.cardmapping[cardtype][nkc]
                dest[nkc] = cardKlass(nkc, klass)

        for crd in dest:
            self.output(f"Playing with {cardtype} {crd}")
        return dest

    ###########################################################################
    def guess_cardname(self, name, prefix="Card"):
        """Don't force the user to give the exact card name on the command
        line - maybe we can guess it"""
        available = self.getAvailableCards(prefix)
        if name in available:
            return name
        for crd in available:
            newc = crd.replace("'", "")
            if newc.lower() == name.lower():
                return crd
            newc = newc.replace(" ", "")
            if newc.lower() == name.lower():
                return crd
            newc = newc.replace(" ", "_")
            if newc.lower() == name.lower():
                return crd
            newc = newc.replace(" ", "-")
            if newc.lower() == name.lower():
                return crd
            name = name.replace("_", "")
            if newc.lower() == name.lower():
                return crd
        return None

    ###########################################################################
    def _place_init_card(self, crd: str, available: list) -> Optional[int]:
        """For the specified card, load it into the correct deck
        Return the number of kingdom cardpiles used or None for not found
        """
        # If basecards are specified by initcards
        if cardname := self.guess_cardname(crd, prefix="BaseCard"):
            cpile = CardPile(cardname, self.cardmapping["BaseCard"][cardname], self)
            self.cardpiles[cpile.name] = cpile
        elif cardname := self.guess_cardname(crd):
            self._use_cardpile(available, cardname, force=True)
            return 1
        elif eventname := self.guess_cardname(crd, "Event"):
            self.eventcards.append(eventname)
        elif wayname := self.guess_cardname(crd, "Way"):
            self.waycards.append(wayname)
        elif landmarkname := self.guess_cardname(crd, "Landmark"):
            self.landmarkcards.append(landmarkname)
        elif projectname := self.guess_cardname(crd, "Project"):
            self.initprojects.append(projectname)
        elif allyname := self.guess_cardname(crd, "Ally"):
            self.init_ally.append(allyname)
        elif self.guess_cardname(crd, "Artifact"):
            # Artifacts should be loaded by the requiring card but can still be specified
            # in a cardset
            pass
        elif crd.lower() == "shelters":
            # Use of shelters handled elsewhere
            pass
        else:
            print(f"Can't guess what card '{crd}' is")
            return None
        return 0

    ###########################################################################
    def _load_decks(self, initcards, numstacks: int):
        """Determine what cards we are using this game"""
        for card in self._base_cards:
            self._use_cardpile(self._base_cards[:], card, force=True, cardtype="BaseCard")
        available = self.getAvailableCards()
        unfilled = numstacks
        foundall = True
        for crd in initcards:
            # These cards get loaded by other things
            if crd in ("Boons",):
                continue
            result = self._place_init_card(crd, available)
            if result is None:
                foundall = False
            else:
                unfilled -= result

        if not foundall:
            sys.exit(1)

        while unfilled:
            if not available:
                # Not enough cards to fill the hand - almost certainly in a test
                break
            crd = random.choice(available)
            if crd in self.badcards:
                continue
            unfilled -= self._use_cardpile(available, crd)

        self._check_card_requirements()

    ###########################################################################
    def _add_prizes(self):
        """TODO"""
        for prize in self.getAvailableCards("PrizeCard"):
            self._use_cardpile(None, prize, False, "PrizeCard")

    ###########################################################################
    def getPrizes(self):
        """TODO"""
        return list(self.cardmapping["PrizeCard"].keys())

    ###########################################################################
    def _use_cardpile(self, available, crd, force=False, cardtype="Card") -> int:
        """TODO"""
        try:
            if available is not None:
                available.remove(crd)
        except ValueError:  # pragma: no cover
            print(f"Unknown card '{crd}'\n", file=sys.stderr)
            sys.exit(1)
        cpile = CardPile(crd, self.cardmapping[cardtype][crd], self)
        if not force and not cpile.insupply:
            return 0
        cpilename = cpile.name
        if hasattr(cpile, "cardpile_setup"):
            cpile = cpile.cardpile_setup(self)
        self.cardpiles[cpilename] = cpile
        for card in cpile:
            self._cards[card.uuid] = card
            card.location = "cardpile"
        self.output(f"Playing with card {self[crd].name}")
        return 1

    ###########################################################################
    def _check_card_requirements(self):
        """If any card we are playing requires another card (e.g. Curse) then
        ensure that is loaded as well"""

        check_cards = (
            list(self._cards.values())
            + list(self.events.values())
            + list(self.hexes)
            + list(self.boons)
            + list(self.landmarks.values())
        )
        if self.ally:
            check_cards.append(self.ally)

        for card in check_cards:
            for x in card.required_cards:
                if isinstance(x, tuple):
                    krdtype, crd = x
                else:
                    krdtype, crd = "BaseCard", x
                if crd not in self.cardpiles:
                    self._use_cardpile(None, crd, force=True, cardtype=krdtype)
                    self.output(f"Playing with {crd} as required by {card.name}")

            if card.heirloom is not None and card.heirloom not in self._heirlooms:
                self._use_cardpile(None, card.heirloom, force=True, cardtype="Heirloom")
                self._heirlooms.append(card.heirloom)
                self.output(f"Playing with {card.heirloom} as required by {card.name}")

            if card.isLooter() and "Ruins" not in self.cardpiles:
                nc = self.numplayers * 10
                self.cardpiles["Ruins"] = RuinCardPile(game=self, pile_size=nc)
                self.output(f"Playing with Ruins as required by {card.name}")
            if card.isFate() and not self.boons:
                self._load_boons()
            if card.isDoom() and not self.hexes:
                self._load_hexes()
                self.output(f"Using hexes as required by {card.name}")
            if card.isLiaison() and not self.ally:
                self._load_ally()
                self.output(f"Using Allies as required by {card.name}")
            if card.traveller and not self.loaded_travellers:
                self._load_travellers()
            if card.needsprize:
                self._add_prizes()
                self.output(f"Playing with Prizes as required by {card.name}")
            if card.needsartifacts and not self.artifacts:
                self._load_artifacts()
                self.output(f"Using artifacts as required by {card.name}")
            if card.needsprojects and not self.projects:
                self._load_projects()
                self.output(f"Using projects as required by {card.name}")
        if self.init_ally and not self.ally:
            print(f"Need to specify a Liaison as well as an Ally {self.init_ally}")
            sys.exit(1)

    ###########################################################################
    def cardTypes(self):
        """TODO"""
        return list(self.cardpiles.values())

    ###########################################################################
    def __getitem__(self, key):
        """Return the card using `game[cardname]`"""
        return self.cardpiles[key]

    ###########################################################################
    def __contains__(self, key):
        """TODO"""
        return key in self.cardpiles

    ###########################################################################
    def _get_available_card_classes(self):
        """Create a mapping between the cardname and the module"""
        mapping = {}
        for prefix in (
            "Card",
            "BaseCard",
            "Traveller",
            "PrizeCard",
            "Castle",
            "Heirloom",
            "Shelter",
        ):
            mapping[prefix] = self.get_card_classes(prefix, self.paths["cards"], "Card_")
            if self.oldcards:
                oldpath = os.path.join(self.paths["cards"], "old")
                mapping[prefix].update(self.get_card_classes(prefix, oldpath, "Card_"))
        mapping["Event"] = self.get_card_classes("Event", self.paths["events"], "Event_")
        mapping["Way"] = self.get_card_classes("Way", self.paths["ways"], "Way_")
        mapping["Landmark"] = self.get_card_classes("Landmark", self.paths["landmarks"], "Landmark_")
        mapping["Boon"] = self.get_card_classes("Boon", self.paths["boons"], "Boon_")
        mapping["Hex"] = self.get_card_classes("Hex", self.paths["hexes"], "Hex_")
        mapping["State"] = self.get_card_classes("State", self.paths["states"], "State_")
        mapping["Artifact"] = self.get_card_classes("Artifact", self.paths["artifacts"], "Artifact_")
        mapping["Project"] = self.get_card_classes("Project", self.paths["projects"], "Project_")
        mapping["Ally"] = self.get_card_classes("Ally", self.paths["allies"], "Ally_")
        return mapping

    ###########################################################################
    @classmethod
    def get_card_classes(cls, prefix, path, class_prefix):
        """Import all the modules to determine the real name of the card
        This is slow, but it is the only way that I can think of

        Look in {path} for files starting with {prefix},
        but also failback to look in {defdir}

        """
        mapping = {}
        files = glob.glob(f"{path}/{prefix}_*.py")
        for fname in [os.path.basename(_) for _ in files]:
            fname = fname.replace(".py", "")
            mod = importlib.import_module(f"{path.replace('/', '.')}.{fname}")

            classes = dir(mod)
            for kls in classes:
                if kls.startswith(class_prefix):
                    klass = getattr(mod, kls)
                    break
            else:  # pragma: no cover
                raise ImportError(f"Couldn't find {prefix} Class in {path}\n")
            mapping[klass().name] = klass
            klass().check()
        return mapping

    ###########################################################################
    def getAvailableCards(self, prefix: str = "Card") -> List[str]:
        """TODO"""
        return list(self.cardmapping[prefix].keys())

    ###########################################################################
    def getActionPiles(self, cost=999):
        """Return all cardstacks that are action cards that cost less than cost"""
        actionpiles = []
        for cpile in self.cardpiles.values():
            if not cpile.purchasable:
                continue
            if cpile.cost > cost:
                continue
            if cpile.isAction():
                actionpiles.append(cpile)
        return actionpiles

    ###########################################################################
    def getTreasurePiles(self):
        """Return all cardstacks that are treasure cards"""
        treasurepiles = []
        for cpile in self.cardpiles.values():
            if cpile.isTreasure():
                treasurepiles.append(cpile)
        return treasurepiles

    ###########################################################################
    def getVictoryPiles(self):
        """Return all cardstacks that are victory cards"""
        victorypiles = []
        for cpile in self.cardpiles.values():
            if cpile.isVictory():
                victorypiles.append(cpile)
        return victorypiles

    ###########################################################################
    def isGameOver(self) -> bool:
        """is the game over"""
        empties = []
        for cpil in self.cardpiles:
            if self[cpil].is_empty():
                empties.append(cpil)
        if len(empties) >= 3:
            self.output(f"Game Over: {', '.join(empties)} piles are empty")
            return True

        if self["Province"].is_empty():
            self.output("Game Over: Province pile is empty")
            return True
        return False

    ###########################################################################
    def receive_hex(self):
        """Receive a hex"""
        if not self.hexes:
            self.cleanup_hexes()
        hx = self.hexes.pop()
        return hx

    ###########################################################################
    def cleanup_hexes(self):
        """TODO"""
        for hx in self.discarded_hexes[:]:
            self.hexes.append(hx)
        random.shuffle(self.hexes)
        self.discarded_hexes = []

    ###########################################################################
    def discard_hex(self, hx):
        """Return a hex"""
        self.discarded_hexes.append(hx)

    ###########################################################################
    def receive_boon(self):
        """Receive a boon"""
        if not self.boons:
            self.boons = self.discarded_boons[:]
            self.discarded_boons = []
            random.shuffle(self.boons)
        boon = self.boons.pop()
        return boon

    ###########################################################################
    def cleanup_boons(self):
        """TODO"""
        for boon in self.retained_boons[:]:
            self.discarded_boons.append(boon)
        self.retained_boons = []
        for boon in self.discarded_boons[:]:
            self.boons.append(boon)
        random.shuffle(self.boons)
        self.discarded_boons = []

    ###########################################################################
    def discard_boon(self, boon):
        """Return a boon"""
        if boon.retain_boon:
            self.retained_boons.append(boon)
        else:
            self.discarded_boons.append(boon)

    ###########################################################################
    def print_player_state(self, plr: Player) -> None:
        """Print the player state for debugging"""
        print("\n")
        print(f"{plr.name} --------------------------")
        print(f"  state: {', '.join([_.name for _ in plr.states])}")
        print(f"  artifacts: {', '.join([_.name for _ in plr.artifacts])}")
        print(f"  projects: {', '.join([_.name for _ in plr.projects])}")
        print(f"  hand: {', '.join([_.name for _ in plr.hand])}")
        print(f"  deck: {', '.join([_.name for _ in plr.deck])}")
        print(f"  discard: {', '.join([_.name for _ in plr.discardpile])}")
        print(f"  defer: {', '.join([_.name for _ in plr.deferpile])}")
        print(f"  duration: {', '.join([_.name for _ in plr.durationpile])}")
        print(f"  exile: {', '.join([_.name for _ in plr.exilepile])}")
        print(f"  reserve: {', '.join([_.name for _ in plr.reserve])}")
        print(f"  played: {', '.join([_.name for _ in plr.played])}")
        print("  messages:")
        for msg in plr.messages:
            print(f"\t{msg}")
        print(f"  score: {plr.get_score()} {plr.get_score_details()}")
        print(f"  tokens: {plr.tokens}")
        print(f"  phase: {plr.phase}")
        print(
            f"  turn: coin={plr.coins.get()} debt={plr.debt.get()} actions={plr.actions.get()}"
            f" buys={plr.buys.get()} favors={plr.favors.get()}"
        )
        print(f"  coffers={plr.coffers.get()} " f"villagers={plr.villagers.get()} potions={plr.potions.get()}")

    ###########################################################################
    def print_state(self, card_dump=False) -> None:  # pragma: no cover
        """This is used for debugging"""
        print("#" * 80)
        print(f"Trash: {', '.join([_.name for _ in self.trashpile])}")
        print(f"Boons: {', '.join([_.name for _ in self.boons])}")
        print(f"Hexes: {', '.join([_.name for _ in self.hexes])}")
        if self.ally:
            print(f"Ally: {self.ally.name}")
        print(f"Projects: {', '.join([_.name for _ in self.projects.values()])}")
        for cname, cpile in self.cardpiles.items():
            tokens = ""
            for plr in self.player_list():
                tkns = plr.which_token(cname)
                if tkns:
                    tokens += f"{plr.name}[{','.join(tkns)}]"

            print(f"CardPile {cname}: {len(cpile)} cards {tokens}")
        for plr in self.player_list():
            self.print_player_state(plr)
        if card_dump:
            for v in self._cards.values():
                print(f"    {v}")

    ###########################################################################
    def player_to_left(self, plr):
        """Return the player to the 'left' of the one specified"""
        players = self.player_list()
        place = players.index(plr) - 1
        return players[place]

    ###########################################################################
    def playerToRight(self, plr):
        """Return the player to the 'right' of the one specified"""
        players = self.player_list()
        place = (players.index(plr) + 1) % len(players)
        return players[place]

    ###########################################################################
    def whoWon(self):
        """TODO"""
        scores = {}
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
    def last_turn(self, plr) -> bool:
        """Who had the last turn"""
        try:
            return self._turns[-1] == plr.uuid
        except IndexError:
            return False

    ###########################################################################
    def _count_all_cards(self) -> dict:  # pragma: no cover
        """Return where all the cards are"""
        tmp = {}
        for pile in self.cardpiles.values():
            tmp[pile.name] = {}
            total = len(pile)
            tmp[pile.name]["pile"] = total
            for plr in self.player_list():
                for stackname, stack in plr.stacklist:
                    count = 0
                    for card in stack:
                        if card.name == pile.name:
                            count += 1
                    if count:
                        tmp[pile.name][f"{plr.name}:{stackname}"] = count
                        total += count
            count = 0
            for card in self.trashpile:
                if card.name == pile.name:
                    count += 1
            if count:
                tmp[pile.name]["trash"] = count
                total += count
            tmp[pile.name]["total"] = total
        return tmp

    ###########################################################################
    def _card_loc_debug(self):
        """Dump info to help debug card location errors"""
        now = self._count_all_cards()
        print(f"{'- -' * 20}", file=sys.stderr)
        print(
            f"current={self.count_cards()} original={self._total_cards}\n",
            file=sys.stderr,
        )
        for pile in self.cardpiles.values():
            card = pile.name
            if self._original[card]["total"] == now[card]["total"]:
                continue
            print(f"{card} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", file=sys.stderr)
            print(f" {card} Original:")
            print(json.dumps(self._original[card], indent=2), file=sys.stderr)
            print(f" {card} Now:")
            print(json.dumps(now[card], indent=2), file=sys.stderr)
        print(f"{'- -' * 20}", file=sys.stderr)

    ###########################################################################
    def turn(self):
        """TODO"""
        try:
            assert self.count_cards() == self._total_cards
            current_cardset = set(self._cards.keys())
            assert self._init_cardset == current_cardset
        except AssertionError:
            self._card_loc_debug()
            raise
        self.current_player = self.player_to_left(self.current_player)
        self.current_player.start_turn()
        self.current_player.turn()
        self.current_player.end_turn()
        self._turns.append(self.current_player.uuid)
        if self.isGameOver():
            self.gameover = True
            for plr in self.player_list():
                plr.game_over()


###############################################################################
class TestGame(Game):
    """Game for testing purposes"""

    def __init__(self, **kwargs):
        if "ally" not in kwargs:
            kwargs["init_ally"] = []
            kwargs["allypath"] = "tests/allies"
        kwargs["shelters"] = False  # Can cause lots of bad interactions
        if "quiet" not in kwargs:
            kwargs["quiet"] = True
        super().__init__(**kwargs)


# EOF

#!/usr/bin/env python
""" Dominion Game Code """
# pylint: disable=too-many-arguments, too-many-branches, too-many-instance-attributes, invalid-name
import argparse
import glob
import imp
import os
import random
import sys
import uuid

from dominion.ArtifactPile import ArtifactPile
from dominion.Ally import AllyPile
from dominion.BoonPile import BoonPile
from dominion.BotPlayer import BotPlayer
from dominion.CardPile import CardPile
from dominion.Event import EventPile
from dominion.HexPile import HexPile
from dominion.LandmarkPile import LandmarkPile
from dominion.Names import playerNames
from dominion.PlayArea import PlayArea
from dominion.ProjectPile import ProjectPile
from dominion.RuinCardPile import RuinCardPile
from dominion.StatePile import StatePile
from dominion.TextPlayer import TextPlayer
from dominion.WayPile import WayPile

# Source of the various cards
ADVENTURE = "adventure"
ALCHEMY = "alchemy"
ALLIES = "allies"
CORNUCOPIA = "cornucopia"
DARKAGES = "darkages"
DOMINION = "dominion"
EMPIRES = "empires"
GUILDS = "guilds"
HINTERLANDS = "hinterlands"
INTRIGUE = "intrigue"
MENAGERIE = "menagerie"
NOCTURNE = "nocturne"
PROMO = "promo"
PROSPERITY = "prosperity"
RENAISSANCE = "renaissance"
SEASIDE = "seaside"


###############################################################################
###############################################################################
###############################################################################
class Game:  # pylint: disable=too-many-public-methods
    """Game class"""

    def __init__(self, **kwargs):

        self.players = {}
        self.cardpiles = {}
        self.states = {}
        self.artifacts = {}
        self.projects = {}
        self.events = {}
        self.ways = {}
        self.landmarks = {}
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
        self.current_player = None
        # The _base_cards are in every game
        self._base_cards = ["Copper", "Silver", "Gold", "Estate", "Duchy", "Province"]
        self.parse_args(**kwargs)
        if self.prosperity:
            self._base_cards.append("Colony")
            self._base_cards.append("Platinum")

        self.cardmapping = self._get_available_card_classes()
        self._total_cards = 0
        self.loaded_travellers = False  # For testing purposes
        self._cards = {}

    ###########################################################################
    def parse_args(self, **args):
        """Parse the arguments passed to the class"""
        self.allypath = args["allypath"] if "allypath" in args else "dominion/allies"
        self.hexpath = "dominion/hexes"
        self.numstacks = args.get("numstacks", 10)
        self.boonpath = args["boonpath"] if "boonpath" in args else "dominion/boons"
        self.statepath = args["statepath"] if "statepath" in args else "dominion/states"
        self.artifactpath = (
            args["artifactpath"] if "artifactpath" in args else "dominion/artifacts"
        )
        self.prosperity = args["prosperity"] if "prosperity" in args else False
        self.oldcards = args.get("oldcards", False)
        self.quiet = args["quiet"] if "quiet" in args else False
        self.numplayers = args["numplayers"] if "numplayers" in args else 2
        self.initcards = args.get("initcards", [])
        self.badcards = args["badcards"] if "badcards" in args else []
        self.cardpath = args["cardpath"] if "cardpath" in args else "dominion/cards"
        self.cardbase = args["cardbase"] if "cardbase" in args else []
        self.bot = args["bot"] if "bot" in args else False

        self.eventcards = args["eventcards"] if "eventcards" in args else []
        self.waycards = args["waycards"] if "waycards" in args else []
        self.eventpath = "dominion/events"
        self.numevents = args["numevents"] if "numevents" in args else 0
        self.waypath = "dominion/ways"
        self.numways = args["numways"] if "numways" in args else 0

        self.landmarkcards = args["landmarkcards"] if "landmarkcards" in args else []
        self.landmarkpath = (
            args["landmarkpath"] if "landmarkpath" in args else "dominion/landmarks"
        )
        self.numlandmarks = args["numlandmarks"] if "numlandmarks" in args else 0

        self.numprojects = args["numprojects"] if "numprojects" in args else 0
        self.projectpath = (
            args["projectpath"] if "projectpath" in args else "dominion/projects"
        )
        self.initprojects = args["initprojects"] if "initprojects" in args else []
        self.init_ally = args["init_ally"] if "init_ally" in args else []
        if not self.init_ally:
            self.init_ally = args["ally"] if "ally" in args else []

    ###########################################################################
    def start_game(self, playernames=None, plrKlass=TextPlayer):
        """Initialise game bits"""
        if playernames is None:
            playernames = []
        names = playerNames[:]
        self._load_decks(self.initcards, self.numstacks)
        self._load_events()
        self._load_ways()
        self._load_landmarks()
        self._load_artifacts()
        self._load_projects()

        if self.hexes or self.boons:
            self._load_states()
        self._check_card_requirements()

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
                )
                self.bot = False
            else:
                self.players[the_uuid] = plrKlass(
                    game=self,
                    quiet=self.quiet,
                    name=name,
                    number=plrnum,
                    heirlooms=self._heirlooms,
                )
            self.players[the_uuid].uuid = the_uuid
        self.card_setup()
        self._total_cards = self.count_cards()
        self._init_cardset = set(self._cards.keys())
        self.current_player = self.player_list(0)
        if self.ally:
            for plr in self.player_list():
                plr.add_favors(1)

    ###########################################################################
    def player_list(self, num=None):
        """TODO"""
        if num is None:
            return list(self.players.values())
        return list(self.players.values())[num]

    ###########################################################################
    def in_trash(self, cardname):
        """Return named card if cardname is in the trash pile"""
        if hasattr(cardname, "name"):
            cardname = cardname.name
        for crd in self.trashpile:
            if crd.name == cardname:
                return crd
        return None

    ###########################################################################
    def set_trash(self, *cards):
        """This is mostly used for testing"""
        self.trashpile.empty()
        for crd in cards:
            self.trashpile.add(self[crd].remove())

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
        count["trash"] = self.trash_size()
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
    def trash_size(self):
        """TODO"""
        return len(self.trashpile)

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
        self.landmarks = self._load_non_kingdom_cards(
            "Landmark", self.landmarkcards, self.numlandmarks, LandmarkPile
        )

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
        self.artifacts = self._load_non_kingdom_cards(
            "Artifact", None, None, ArtifactPile
        )

    ###########################################################################
    def _load_projects(self):
        """TODO"""
        if self.projects:
            return
        self.projects = self._load_non_kingdom_cards(
            "Project", self.initprojects, self.numprojects, ProjectPile
        )

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
        return None

    ###########################################################################
    def _load_decks(self, initcards, numstacks: int):
        """Determine what cards we are using this game"""
        for card in self._base_cards:
            self._use_cardpile(
                self._base_cards[:], card, force=True, cardtype="BaseCard"
            )
        available = self.getAvailableCards()
        unfilled = numstacks
        foundall = True
        for crd in initcards:
            # If basecards are specified by initcards
            cardname = self.guess_cardname(crd, prefix="BaseCard")
            if cardname:
                cpile = CardPile(cardname, self.cardmapping["BaseCard"][cardname], self)
                self.cardpiles[cpile.name] = cpile
                continue
            cardname = self.guess_cardname(crd)
            if cardname:
                self._use_cardpile(available, cardname, force=True)
                unfilled -= 1
                continue
            eventname = self.guess_cardname(crd, "Event")
            if eventname:
                self.eventcards.append(eventname)
                continue

            wayname = self.guess_cardname(crd, "Way")
            if wayname:
                self.waycards.append(wayname)
                continue

            landmarkname = self.guess_cardname(crd, "Landmark")
            if landmarkname:
                self.landmarkcards.append(landmarkname)
                continue
            projectname = self.guess_cardname(crd, "Project")
            if projectname:
                self.initprojects.append(projectname)
                continue
            allyname = self.guess_cardname(crd, "Ally")
            if allyname:
                self.init_ally.append(allyname)
                continue
            print(f"Can't guess what card '{crd}' is")
            foundall = False
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
        # print(f"DBG _use_cardpile({crd=}, {force=}, {cardtype=})")
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
        ):
            mapping[prefix] = self.getSetCardClasses(
                prefix, self.cardpath, "cards", "Card_"
            )
            if self.oldcards:
                oldpath = os.path.join(self.cardpath, "old")
                mapping[prefix].update(
                    self.getSetCardClasses(prefix, oldpath, "cards", "Card_")
                )
        mapping["Event"] = self.getSetCardClasses(
            "Event", self.eventpath, "events", "Event_"
        )
        mapping["Way"] = self.getSetCardClasses("Way", self.waypath, "ways", "Way_")
        mapping["Landmark"] = self.getSetCardClasses(
            "Landmark", self.landmarkpath, "landmarks", "Landmark_"
        )
        mapping["Boon"] = self.getSetCardClasses(
            "Boon", self.boonpath, "boons", "Boon_"
        )
        mapping["Hex"] = self.getSetCardClasses("Hex", self.hexpath, "hexes", "Hex_")
        mapping["State"] = self.getSetCardClasses(
            "State", self.statepath, "states", "State_"
        )
        mapping["Artifact"] = self.getSetCardClasses(
            "Artifact", self.artifactpath, "artifacts", "Artifact_"
        )
        mapping["Project"] = self.getSetCardClasses(
            "Project", self.projectpath, "projects", "Project_"
        )
        mapping["Ally"] = self.getSetCardClasses(
            "Ally", self.allypath, "allies", "Ally_"
        )
        return mapping

    ###########################################################################
    @classmethod
    def getSetCardClasses(cls, prefix, path, defdir, class_prefix):
        """Import all the modules to determine the real name of the card
        This is slow, but it is the only way that I can think of

        Look in {path} for files starting with {prefix},
        but also failback to look in {defdir}

        """
        mapping = {}
        files = glob.glob(f"{path}/{prefix}_*.py")
        for fname in [os.path.basename(_) for _ in files]:
            fname = fname.replace(".py", "")
            fp, pathname, desc = imp.find_module(fname, [path, defdir])
            mod = imp.load_module(fname, fp, pathname, desc)
            fp.close()
            classes = dir(mod)
            for kls in classes:
                if kls.startswith(class_prefix):
                    klass = getattr(mod, kls)
                    break
            else:  # pragma: no cover
                sys.stderr.write(f"Couldn't find {prefix} Class in {pathname}\n")
            mapping[klass().name] = klass
            klass().check()
        return mapping

    ###########################################################################
    def getAvailableCards(self, prefix="Card"):
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
    def getVictoryPiles(self):
        """Return all cardstacks that are victory cards"""
        victorypiles = []
        for cpile in self.cardpiles.values():
            if cpile.isVictory():
                victorypiles.append(cpile)
        return victorypiles

    ###########################################################################
    def isGameOver(self):
        """TODO"""
        numEmpty = 0
        for cpil in self.cardpiles:
            if self[cpil].is_empty():
                numEmpty += 1
        if numEmpty >= 3:
            return True

        if self["Province"].is_empty():
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
    def print_state(self):  # pragma: no cover
        """This is used for debugging"""
        print("#" * 40)
        print(f"Trash: {', '.join([_.name for _ in self.trashpile])}")
        print(f"Boons: {', '.join([_.name for _ in self.boons])}")
        print(f"Hexes: {', '.join([_.name for _ in self.hexes])}")
        if self.ally:
            print(f"Ally: {self.ally.name}")
        print(f"Projects: {', '.join([_.name for _ in self.projects.values()])}")
        for cpile in self.cardpiles:
            tokens = ""
            for plr in self.player_list():
                tkns = plr.which_token(cpile)
                if tkns:
                    tokens += f"{plr.name}[{','.join(tkns)}]"

            print(f"CardPile {cpile}: %d cards {tokens}" % len(self.cardpiles[cpile]))
        for plr in self.player_list():
            print(
                f"\n{plr.name}'s state: %s" % (", ".join([s.name for s in plr.states]))
            )
            print(
                f"  {plr.name}'s artifacts: %s"
                % (", ".join([_.name for _ in plr.artifacts]))
            )
            print(
                f"  {plr.name}'s projects: %s"
                % (", ".join([_.name for _ in plr.projects]))
            )
            print(f"  {plr.name}'s hand: %s" % (", ".join([_.name for _ in plr.hand])))
            print(f"  {plr.name}'s deck: %s" % (", ".join([_.name for _ in plr.deck])))
            print(
                f"  {plr.name}'s discard: %s"
                % (", ".join([_.name for _ in plr.discardpile]))
            )
            print(
                f"  {plr.name}'s defer: %s"
                % (", ".join([_.name for _ in plr.deferpile]))
            )
            print(
                f"  {plr.name}'s duration: %s"
                % (", ".join([_.name for _ in plr.durationpile]))
            )
            print(
                f"  {plr.name}'s exile: %s"
                % (", ".join([_.name for _ in plr.exilepile]))
            )
            print(
                f"  {plr.name}'s reserve: %s"
                % (", ".join([_.name for _ in plr.reserve]))
            )
            print(
                f"  {plr.name}'s played: %s" % (", ".join([_.name for _ in plr.played]))
            )
            print(f"  {plr.name}'s messages: %s" % (plr.messages))
            print(
                f"  {plr.name}'s score: %s %s"
                % (plr.get_score(), plr.get_score_details())
            )
            print(f"  {plr.name}'s tokens: %s" % (plr.tokens))
            print(
                f"  {plr.name}'s turn: coin={plr.coin} debt={plr.debt} actions={plr.actions}"
                f" buys={plr.buys} favors={plr.favors}"
            )
            print(
                f"  {plr.name}: coffers=%d villagers=%d potions=%d"
                % (plr.coffer, plr.villager, plr.potions)
            )
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
        self.output(scores)
        self.output("")
        for plr in self.player_list():
            self.output(f"Cards of {plr.name}:")
            for k, v in plr.get_cards().items():
                self.output(f"{plr.name}: {k}={v}")
        self.output("Trash: %s" % ", ".join([_.name for _ in self.trashpile]))
        return scores

    ###########################################################################
    def last_turn(self, plr) -> bool:
        """ Who had the last turn """
        try:
            return self._turns[-1] == plr.uuid
        except IndexError:
            return False

    ###########################################################################
    def count_all_cards(self):  # pragma: no cover
        """TODO"""
        for pile in self.cardpiles.values():
            total = len(pile)
            sys.stderr.write("%-15s  " % pile.name)
            if total:
                sys.stderr.write(f"pile={total} ")
            for plr in self.player_list():
                for stackname, stack in plr.stacklist:
                    count = 0
                    for card in stack:
                        if card.name == pile.name:
                            count += 1
                    total += count
                    if count:
                        sys.stderr.write("%s:%s=%s " % (plr.name, stackname, count))
            count = 0
            for card in self.trashpile:
                if card.name == pile.name:
                    count += 1
            if count:
                sys.stderr.write(f"Trash={count} ")
            total += count
            sys.stderr.write(f" = {total}\n")

    ###########################################################################
    def turn(self):
        """TODO"""
        try:
            assert self.count_cards() == self._total_cards
            current_cardset = set(self._cards.keys())
            assert self._init_cardset == current_cardset
        except AssertionError:
            self.count_all_cards()
            print(f"current = {self.count_cards()}\n", file=sys.stderr)
            sys.stderr.write(f"original = {self._total_cards}\n")
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
    """ Game for testing purposes """
    def __init__(self, **kwargs):
        if "ally" not in kwargs:
            kwargs["init_ally"] = "noop"
            kwargs["ally"] = "noop"
            kwargs["allypath"] = "tests/allies"
        if "quiet" not in kwargs:
            kwargs["quiet"] = True
        super().__init__(**kwargs)


###############################################################################
def parse_cli_args(args=None):
    """Parse the command line arguments"""
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Play dominion")
    parser.add_argument("--numplayers", type=int, default=2, help="How many players")
    parser.add_argument(
        "--card",
        action="append",
        dest="initcards",
        default=[],
        help="Include card in lineup",
    )
    parser.add_argument(
        "--bad",
        action="append",
        dest="badcards",
        default=[],
        help="Do not include card in lineup",
    )
    parser.add_argument(
        "--numevents", type=int, default=0, help="Number of events to use"
    )
    parser.add_argument(
        "--events", action="append", dest="eventcards", default=[], help="Include event"
    )
    parser.add_argument("--numways", type=int, default=0, help="Number of ways to use")
    parser.add_argument(
        "--ways", action="append", dest="waycards", default=[], help="Include way"
    )

    parser.add_argument(
        "--numlandmarks", type=int, default=0, help="Number of landmarks to use"
    )
    parser.add_argument(
        "--landmark",
        action="append",
        dest="landmarkcards",
        default=[],
        help="Include landmark",
    )
    parser.add_argument(
        "--landmarkpath", default="dominion/landmarks", help=argparse.SUPPRESS
    )

    parser.add_argument(
        "--numprojects", type=int, default=0, help="Number of projects to use"
    )
    parser.add_argument(
        "--oldcards", action="store_true", default=False, help="Use cards from retired versions"
    )
    parser.add_argument(
        "--project",
        action="append",
        dest="initprojects",
        default=[],
        help="Include project",
    )
    parser.add_argument(
        "--projectpath", default="dominion/projects", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--ally",
        dest="init_ally",
        action="append",
        default=[],
        help="Include specific ally",
    )
    parser.add_argument(
        "--cardset",
        type=argparse.FileType("r"),
        help="File containing list of cards to use",
    )
    parser.add_argument(
        "--cardbase", action="append", help="Include only cards from the specified base"
    )
    parser.add_argument(
        "--cardpath", default="dominion/cards", help="Where to find card definitions"
    )
    parser.add_argument(
        "--artifactpath", default="dominion/artifacts", help=argparse.SUPPRESS
    )
    parser.add_argument("--boonpath", default="dominion/boons", help=argparse.SUPPRESS)
    parser.add_argument("--numstacks", default=10, help=argparse.SUPPRESS)
    parser.add_argument(
        "--prosperity",
        default=False,
        action="store_true",
        help="Use colonies and platinums",
    )
    parser.add_argument(
        "--bot", action="store_true", dest="bot", default=False, help="Bot Player"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        dest="quiet",
        default=False,
        help="Supress a lot of output",
    )
    namespace = parser.parse_args(args)
    return namespace


###############################################################################
def runGame(args):  # pragma: no cover
    """TODO"""
    cards = args["initcards"]
    if args["cardset"]:
        for line in args["cardset"]:
            if line.startswith("--prosperity"):
                args["prosperity"] = True
            if line.startswith("--oldcards"):
                args["oldcards"] = True
            cards.append(line.strip())
    args["initcards"] = cards
    g = Game(**args)
    g.start_game()
    try:
        while not g.gameover:
            try:
                g.turn()
            except Exception:
                g.print_state()
                raise
    except KeyboardInterrupt:
        g.gameover = True
    g.whoWon()


###############################################################################
def main():  # pragma: no cover
    """Command line entry point"""
    args = parse_cli_args()
    runGame(vars(args))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    main()

# EOF

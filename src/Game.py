#!/usr/bin/env python
""" Dominion Game Code """
# pylint: disable=too-many-arguments, too-many-branches, too-many-instance-attributes
import argparse
import glob
import imp
import os
import random
import sys
import uuid

from ArtifactPile import ArtifactPile
from BoonPile import BoonPile
from BotPlayer import BotPlayer
from CardPile import CardPile
from EventPile import EventPile
from HexPile import HexPile
from LandmarkPile import LandmarkPile
from Names import playerNames
from PlayArea import PlayArea
from PrizeCardPile import PrizeCardPile
from ProjectPile import ProjectPile
from RuinCardPile import RuinCardPile
from StatePile import StatePile
from TextPlayer import TextPlayer
from WayPile import WayPile


###############################################################################
###############################################################################
###############################################################################
class Game(object):     # pylint: disable=too-many-public-methods
    """ Game class """
    def __init__(self, **kwargs):
        self.parse_args(**kwargs)

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
        self.discarded_hexes = []
        self.trashpile = PlayArea([])
        self.gameover = False
        self.current_player = None
        self.base_cards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']
        if self.prosperity:
            self.base_cards.append('Colony')
            self.base_cards.append('Platinum')
        self.cardmapping = self.getAvailableCardClasses()
        self.total_cards = 0
        self.loaded_travellers = False  # For testing purposes

    ###########################################################################
    def parse_args(self, **args):
        """ Parse the arguments passed to the class """
        self.hexpath = 'hexes'
        self.numstacks = args['numstacks'] if 'numstacks' in args else 10
        self.boonpath = args['boonpath'] if 'boonpath' in args else 'boons'
        self.statepath = args['statepath'] if 'statepath' in args else 'states'
        self.artifactpath = args['artifactpath'] if 'artifactpath' in args else 'artifacts'
        self.prosperity = args['prosperity'] if 'prosperity' in args else False
        self.quiet = args['quiet'] if 'quiet' in args else False
        self.numplayers = args['numplayers'] if 'numplayers' in args else 2
        self.initcards = args['initcards'] if 'initcards' in args else []
        self.badcards = args['badcards'] if 'badcards' in args else []
        self.cardpath = args['cardpath'] if 'cardpath' in args else 'cards'
        self.cardbase = args['cardbase'] if 'cardbase' in args else []
        self.bot = args['bot'] if 'bot' in args else False

        self.eventcards = args['eventcards'] if 'eventcards' in args else []
        self.waycards = args['waycards'] if 'waycards' in args else []
        self.eventpath = 'events'
        self.numevents = args['numevents'] if 'numevents' in args else 0
        self.waypath = 'ways'
        self.numways = args['numways'] if 'numways' in args else 0

        self.landmarkcards = args['landmarkcards'] if 'landmarkcards' in args else []
        self.landmarkpath = args['landmarkpath'] if 'landmarkpath' in args else 'landmarks'
        self.numlandmarks = args['numlandmarks'] if 'numlandmarks' in args else 0

        self.numprojects = args['numprojects'] if 'numprojects' in args else 0
        self.projectpath = args['projectpath'] if 'projectpath' in args else 'projects'
        self.initprojects = args['initprojects'] if 'initprojects' in args else []

    ###########################################################################
    def start_game(self, playernames=None, plrKlass=TextPlayer):
        """ Initialise game bits """
        if playernames is None:
            playernames = []
        names = playerNames[:]
        self.loadDecks(self.initcards, self.numstacks)
        self.loadEvents()
        self.loadWays()
        self.loadLandmarks()
        self.loadArtifacts()
        self.loadProjects()
        heirlooms = self.enable_heirlooms()

        if self.hexes or self.boons:
            self.loadStates()
        self.checkCardRequirements()

        for plrnum in range(self.numplayers):
            try:
                name = playernames.pop()
            except IndexError:
                name = random.choice(names)
                names.remove(name)
            the_uuid = uuid.uuid4().hex
            if self.bot:
                self.players[the_uuid] = BotPlayer(
                    game=self, quiet=self.quiet, name='%sBot' % name, heirlooms=heirlooms
                )
                self.bot = False
            else:
                self.players[the_uuid] = plrKlass(game=self, quiet=self.quiet, name=name, number=plrnum, heirlooms=heirlooms)
            self.players[the_uuid].uuid = the_uuid
        self.card_setup()
        self.total_cards = self.countCards()
        self.current_player = self.player_list(0)

    ###########################################################################
    def player_list(self, num=None):
        """ TODO """
        if num is None:
            return list(self.players.values())
        return list(self.players.values())[num]

    ###########################################################################
    def in_trash(self, cardname):
        """ Return named card if cardname is in the trash pile """
        if hasattr(cardname, 'name'):
            cardname = cardname.name
        for crd in self.trashpile:
            if crd.name == cardname:
                return crd
        return None

    ###########################################################################
    def set_trash(self, *cards):
        """ This is mostly used for testing """
        self.trashpile.empty()
        for crd in cards:
            self.trashpile.add(self[crd].remove())

    ###########################################################################
    def card_setup(self):
        """ Run the setup() method for all cards """
        for cpile in list(self.cardpiles.values()):
            cpile.setup(game=self)
        for lm in list(self.landmarks.values()):
            lm.setup(game=self)

    ###########################################################################
    def countCards(self):
        """ TODO """
        count = {}
        count['trash'] = self.trashSize()
        for cpile in list(self.cardpiles.values()):
            count['pile_%s' % cpile.name] = cpile.pilesize
        for pl in self.player_list():
            count['player_%s' % pl.name] = pl.countCards()
        total = sum(count.values())
        return total

    ###########################################################################
    def output(self, msg):
        """ Send output to all players """
        if not self.quiet:
            sys.stdout.write("ALL: %s\n" % msg)

    ###########################################################################
    def trashSize(self):
        """ TODO """
        return len(self.trashpile)

    ###########################################################################
    def loadTravellers(self):
        """ TODO """
        travellers = self.getAvailableCards('Traveller')
        for trav in travellers:
            cpile = CardPile(trav, self.cardmapping['Traveller'][trav], self)
            self.cardpiles[cpile.name] = cpile
        self.loaded_travellers = True

    ###########################################################################
    def loadWays(self):
        """ TODO """
        self.loadNonKingdomCards('Way', self.waycards, self.numways, WayPile, self.ways)

    ###########################################################################
    def loadEvents(self):
        """ TODO """
        self.loadNonKingdomCards('Event', self.eventcards, self.numevents, EventPile, self.events)

    ###########################################################################
    def loadLandmarks(self):
        """ TODO """
        self.loadNonKingdomCards('Landmark', self.landmarkcards, self.numlandmarks, LandmarkPile, self.landmarks)

    ###########################################################################
    def loadBoons(self):
        """ TODO """
        if self.boons:
            return
        self.output("Using boons")
        d = {}
        self.loadNonKingdomCards('Boon', None, None, BoonPile, d)
        self.boons = list(d.values())
        random.shuffle(self.boons)

    ###########################################################################
    def loadHexes(self):
        """ TODO """
        if self.hexes:
            return
        d = {}
        self.output("Using hexes")
        self.loadNonKingdomCards('Hex', None, None, HexPile, d)
        self.hexes = list(d.values())
        random.shuffle(self.hexes)

    ###########################################################################
    def loadStates(self):
        """ TODO """
        if self.states:
            return
        self.output("Using states")
        self.loadNonKingdomCards('State', None, None, StatePile, self.states)

    ###########################################################################
    def loadArtifacts(self):
        """ TODO """
        if self.artifacts:
            return
        self.output("Using artifacts")
        self.loadNonKingdomCards('Artifact', None, None, ArtifactPile, self.artifacts)

    ###########################################################################
    def loadProjects(self):
        """ TODO """
        if self.projects:
            return
        self.output("Using projects")
        self.loadNonKingdomCards('Project', self.initprojects, self.numprojects, ProjectPile, self.projects)

    ###########################################################################
    def loadNonKingdomCards(self, cardtype, specified, numspecified, cardKlass, dest):
        """ TODO """
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
                    sys.stderr.write("Unknown %s '%s'\n" % (cardtype, nkc))
                    sys.exit(1)
        if numspecified is not None:
            # To make up the numbers
            while len(dest) < numspecified:
                nkc = random.choice(available)
                klass = self.cardmapping[cardtype][nkc]
                dest[nkc] = cardKlass(nkc, klass)
                available.remove(nkc)
        else:
            for nkc in available:
                klass = self.cardmapping[cardtype][nkc]
                dest[nkc] = cardKlass(nkc, klass)

        for crd in dest:
            self.output("Playing with %s %s" % (cardtype, crd))

    ###########################################################################
    def guess_cardname(self, name, prefix='Card'):
        """ Don't force the user to give the exact card name on the command
        line - maybe we can guess it """
        available = self.getAvailableCards(prefix)
        if prefix == 'Way':
            name = name.replace('Way of the ', '')
        if name in available:
            return name
        for crd in available:
            newc = crd.replace("'", "")
            if newc.lower() == name.lower():
                return crd
            newc = newc.replace(' ', '')
            if newc.lower() == name.lower():
                return crd
        return None

    ###########################################################################
    def loadDecks(self, initcards, numstacks):
        """ TODO """
        for card in self.base_cards:
            cpile = CardPile(card, self.cardmapping['BaseCard'][card], self)
            self.cardpiles[cpile.name] = cpile
        available = self.getAvailableCards()
        unfilled = numstacks
        foundall = True
        for crd in initcards:
            cardname = self.guess_cardname(crd)
            if cardname:
                self.useCardPile(available, cardname, force=True)
                unfilled -= 1
                continue
            eventname = self.guess_cardname(crd, 'Event')
            if eventname:
                self.eventcards.append(eventname)
                continue
            wayname = self.guess_cardname(crd, 'Way')
            if wayname:
                self.waycards.append(wayname)
                continue
            landmarkname = self.guess_cardname(crd, 'Landmark')
            if landmarkname:
                self.landmarkcards.append(landmarkname)
                continue
            projectname = self.guess_cardname(crd, 'Project')
            if projectname:
                self.initprojects.append(projectname)
                continue
            print("Can't guess what card '%s' is" % crd)
            foundall = False
        if not foundall:
            sys.exit(1)

        while unfilled:
            crd = random.choice(available)
            if crd in self.badcards:
                continue
            unfilled -= self.useCardPile(available, crd)

        self.checkCardRequirements()

    ###########################################################################
    def addPrizes(self):
        """ TODO """
        for prize in self.getAvailableCards('PrizeCard'):
            self.cardpiles[prize] = PrizeCardPile(prize, self.cardmapping['PrizeCard'][prize])
        self.output("Playing with Prizes")

    ###########################################################################
    def getPrizes(self):
        """ TODO """
        return list(self.cardmapping['PrizeCard'].keys())

    ###########################################################################
    def useCardPile(self, available, crd, force=False):
        """ TODO """
        try:
            available.remove(crd)
        except ValueError:  # pragma: no cover
            sys.stderr.write("Unknown card '%s'\n" % crd)
            sys.exit(1)
        cpile = CardPile(crd, self.cardmapping['Card'][crd], self)
        if not force and not cpile.insupply:
            return 0
        self.cardpiles[cpile.name] = cpile
        self.output("Playing with card %s" % self[crd].name)
        return 1

    ###########################################################################
    def enable_heirlooms(self):
        """ Go through the cardpiles and see if any require heirloom cards
        to be brought into the game """
        heirlooms = set()
        for card in list(self.cardpiles.values()):
            if card.heirloom is not None:
                heirlooms.add(card.heirloom)
                cpile = CardPile(card.heirloom, self.cardmapping['Heirloom'][card.heirloom], self)
                self.cardpiles[cpile.name] = cpile

        return list(heirlooms)

    ###########################################################################
    def checkCardRequirements(self):
        """ TODO """
        for card in list(self.cardpiles.values()) + list(self.events.values()) + list(self.hexes) + list(self.boons):
            for x in card.required_cards:
                if isinstance(x, tuple):
                    k, crd = x
                else:
                    k, crd = 'BaseCard', x
                if crd not in self.cardpiles:
                    self.cardpiles[crd] = CardPile(crd, self.cardmapping[k][crd], self)
                    self.output("Playing with %s" % crd)

        for card in self.landmarks.values():
            for x in card.required_cards:
                if isinstance(x, tuple):
                    k, crd = x
                else:
                    k, crd = 'BaseCard', x
                if crd not in self.cardpiles:
                    self.cardpiles[crd] = CardPile(crd, self.cardmapping[k][crd], self)
                    self.output("Playing with %s" % crd)

        for card in list(self.cardpiles.keys()):
            if self.cardpiles[card].isLooter() and 'Ruins' not in self.cardpiles:
                nc = self.numplayers * 10
                self.cardpiles['Ruins'] = RuinCardPile(self.cardmapping['RuinCard'], pilesize=nc)
                self.output("Playing with Ruins")
            if self.cardpiles[card].isFate() and not self.boons:
                self.loadBoons()
            if self.cardpiles[card].isDoom() and not self.hexes:
                self.loadHexes()
            if self.cardpiles[card].traveller:
                self.loadTravellers()
            if self.cardpiles[card].needsprize:
                self.addPrizes()
            if self.cardpiles[card].needsartifacts:
                self.loadArtifacts()
            if self.cardpiles[card].needsprojects:
                self.loadProjects()

    ###########################################################################
    def cardTypes(self):
        """ TODO """
        return list(self.cardpiles.values())

    ###########################################################################
    def __getitem__(self, key):
        """ TODO """
        return self.cardpiles[key]

    ###########################################################################
    def __contains__(self, key):
        """ TODO """
        return key in self.cardpiles

    ###########################################################################
    def getAvailableCardClasses(self):
        """ Create a mapping between the cardname and the module """
        mapping = {}
        for prefix in ('Card', 'Traveller', 'BaseCard', 'RuinCard', 'PrizeCard', 'KnightCard', 'Castle', 'Heirloom'):
            mapping[prefix] = self.getSetCardClasses(prefix, self.cardpath, 'cards', 'Card_')
        mapping['Event'] = self.getSetCardClasses('Event', self.eventpath, 'events', 'Event_')
        mapping['Way'] = self.getSetCardClasses('Way', self.waypath, 'ways', 'Way_')
        mapping['Landmark'] = self.getSetCardClasses('Landmark', self.landmarkpath, 'landmarks', 'Landmark_')
        mapping['Boon'] = self.getSetCardClasses('Boon', self.boonpath, 'boons', 'Boon_')
        mapping['Hex'] = self.getSetCardClasses('Hex', self.hexpath, 'hexes', 'Hex_')
        mapping['State'] = self.getSetCardClasses('State', self.statepath, 'states', 'State_')
        mapping['Artifact'] = self.getSetCardClasses('Artifact', self.artifactpath, 'artifacts', 'Artifact_')
        mapping['Project'] = self.getSetCardClasses('Project', self.projectpath, 'projects', 'Project_')
        return mapping

    ###########################################################################
    def getSetCardClasses(self, prefix, path, defdir, class_prefix):
        """ Import all the modules to determine the real name of the card
            This is slow, but it is the only way that I can think of """
        mapping = {}
        files = glob.glob('%s/%s_*.py' % (path, prefix))
        for fname in [os.path.basename(_) for _ in files]:
            fname = fname.replace('.py', '')
            fp, pathname, desc = imp.find_module(fname, [path, defdir])
            mod = imp.load_module(fname, fp, pathname, desc)
            fp.close()
            classes = dir(mod)
            for kls in classes:
                if kls.startswith(class_prefix):
                    klass = getattr(mod, kls)
                    break
            else:   # pragma: no cover
                sys.stderr.write("Couldn't find %s Class in %s\n" % (prefix, pathname))
            mapping[klass().name] = klass
        return mapping

    ###########################################################################
    def getAvailableCards(self, prefix='Card'):
        """ TODO """
        return list(self.cardmapping[prefix].keys())

    ###########################################################################
    def getActionPiles(self, cost=999):
        """ Return all cardstacks that are action cards that cost less than cost """
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
        """ Return all cardstacks that are victory cards """
        victorypiles = []
        for cpile in self.cardpiles.values():
            if cpile.isVictory():
                victorypiles.append(cpile)
        return victorypiles

    ###########################################################################
    def isGameOver(self):
        """ TODO """
        numEmpty = 0
        for cpil in self.cardpiles:
            if self[cpil].isEmpty():
                numEmpty += 1
        if numEmpty >= 3:
            return True

        if self['Province'].isEmpty():
            return True
        return False

    ###########################################################################
    def receive_hex(self):
        """ Receive a hex """
        if not self.hexes:
            self.cleanup_hexes()
        hx = self.hexes.pop()
        return hx

    ###########################################################################
    def cleanup_hexes(self):
        """ TODO """
        for hx in self.discarded_hexes[:]:
            self.hexes.append(hx)
        random.shuffle(self.hexes)
        self.discarded_hexes = []

    ###########################################################################
    def discard_hex(self, hx):
        """ Return a hex """
        self.discarded_hexes.append(hx)

    ###########################################################################
    def receive_boon(self):
        """ Receive a boon """
        if not self.boons:
            self.boons = self.discarded_boons[:]
            self.discarded_boons = []
            random.shuffle(self.boons)
        boon = self.boons.pop()
        return boon

    ###########################################################################
    def cleanup_boons(self):
        """ TODO """
        for boon in self.retained_boons[:]:
            self.discarded_boons.append(boon)
        self.retained_boons = []
        for boon in self.discarded_boons[:]:
            self.boons.append(boon)
        random.shuffle(self.boons)
        self.discarded_boons = []

    ###########################################################################
    def discard_boon(self, boon):
        """ Return a boon """
        if boon.retain_boon:
            self.retained_boons.append(boon)
        else:
            self.discarded_boons.append(boon)

    ###########################################################################
    def print_state(self):  # pragma: no cover
        """ This is used for debugging """
        print("#" * 40)
        print("Trash: %s" % ", ".join([_.name for _ in self.trashpile]))
        print("Boons: {}".format(", ".join([_.name for _ in self.boons])))
        print("Hexes: {}".format(", ".join([_.name for _ in self.hexes])))
        print("Projects: {}".format(", ".join([_.name for _ in self.projects.values()])))
        for cpile in self.cardpiles:
            tokens = ""
            for plr in self.player_list():
                tkns = plr.which_token(cpile)
                if tkns:
                    tokens += "%s[%s]" % (plr.name, ",".join(tkns))

            print("CardPile %s: %d cards %s" % (cpile, self.cardpiles[cpile].pilesize, tokens))
        for plr in self.player_list():
            print("\n%s's state: %s" % (plr.name, ", ".join([s.name for s in plr.states])))
            print("  %s's artifacts: %s" % (plr.name, ", ".join([_.name for _ in plr.artifacts])))
            print("  %s's projects: %s" % (plr.name, ", ".join([_.name for _ in plr.projects])))
            print("  %s's hand: %s" % (plr.name, ", ".join([_.name for _ in plr.hand])))
            print("  %s's deck: %s" % (plr.name, ", ".join([_.name for _ in plr.deck])))
            print("  %s's discard: %s" % (plr.name, ", ".join([_.name for _ in plr.discardpile])))
            print("  %s's duration: %s" % (plr.name, ", ".join([_.name for _ in plr.durationpile])))
            print("  %s's exile: %s" % (plr.name, ", ".join([_.name for _ in plr.exilepile])))
            print("  %s's reserve: %s" % (plr.name, ", ".join([_.name for _ in plr.reserve])))
            print("  %s's played: %s" % (plr.name, ", ".join([_.name for _ in plr.played])))
            print("  %s's messages: %s" % (plr.name, plr.messages))
            print("  %s's score: %s %s" % (plr.name, plr.getScore(), plr.getScoreDetails()))
            print("  %s's tokens: %s" % (plr.name, plr.tokens))
            print("  %s's turn: coin=%d debt=%d actions=%d buys=%d" % (plr.name, plr.coin, plr.debt, plr.actions, plr.buys))
            print("  %s: coffers=%d villagers=%d potions=%d" % (plr.name, plr.coffer, plr.villager, plr.potions))

    ###########################################################################
    def playerToLeft(self, plr):
        """ Return the player to the 'left' of the one specified """
        players = self.player_list()
        place = players.index(plr) - 1
        return players[place]

    ###########################################################################
    def playerToRight(self, plr):
        """ Return the player to the 'right' of the one specified """
        players = self.player_list()
        place = (players.index(plr) + 1) % len(players)
        return players[place]

    ###########################################################################
    def whoWon(self):
        """ TODO """
        scores = {}
        self.output("")
        self.output("Scores:")
        for plr in self.player_list():
            scores[plr.name] = plr.getScore(verbose=True)
        self.output(scores)
        self.output("")
        for plr in self.player_list():
            self.output("Cards of %s:" % plr.name)
            for k, v in plr.getCards().items():
                self.output("%s: %s=%s" % (plr.name, k, v))
        self.output("Trash: %s" % ", ".join([_.name for _ in self.trashpile]))
        return scores

    ###########################################################################
    def count_all_cards(self):  # pragma: no cover
        """ TODO """
        for pile in self.cardpiles.values():
            total = pile.pilesize
            sys.stderr.write("%-15s  " % pile.name)
            if total:
                sys.stderr.write("pile=%d " % total)
            for plr in self.player_list():
                stacklist = (
                    ('Discard', plr.discardpile), ('Hand', plr.hand),
                    ('Reserve', plr.reserve), ('Deck', plr.deck),
                    ('Played', plr.played), ('Duration', plr.durationpile))
                for stackname, stack in stacklist:
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
                sys.stderr.write("Trash=%s " % count)
            total += count
            sys.stderr.write(" = %d\n" % total)

    ###########################################################################
    def turn(self):
        """ TODO """
        try:
            assert self.countCards() == self.total_cards
        except AssertionError:
            self.count_all_cards()
            sys.stderr.write("current = %s\n" % self.countCards())
            sys.stderr.write("original = %d\n" % self.total_cards)
            raise
        self.current_player = self.playerToLeft(self.current_player)
        self.current_player.startTurn()
        self.current_player.turn()
        self.current_player.end_turn()
        if self.isGameOver():
            self.gameover = True
            for plr in self.player_list():
                plr.gameOver()


###############################################################################
def parse_cli_args(args=None):
    """ Parse the command line arguments """
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Play dominion')
    parser.add_argument('--numplayers', type=int, default=2,
                        help='How many players')
    parser.add_argument('--card', action='append', dest='initcards',
                        default=[],
                        help='Include card in lineup')
    parser.add_argument('--bad', action='append', dest='badcards',
                        default=[],
                        help='Do not include card in lineup')
    parser.add_argument('--numevents', type=int, default=0,
                        help='Number of events to use')
    parser.add_argument('--events', action='append', dest='eventcards',
                        default=[],
                        help='Include event')
    parser.add_argument('--numways', type=int, default=0,
                        help='Number of ways to use')
    parser.add_argument('--ways', action='append', dest='waycards',
                        default=[],
                        help='Include way')

    parser.add_argument('--numlandmarks', type=int, default=0,
                        help='Number of landmarks to use')
    parser.add_argument('--landmark', action='append', dest='landmarkcards',
                        default=[],
                        help='Include landmark')
    parser.add_argument('--landmarkpath', default='landmarks', help=argparse.SUPPRESS)

    parser.add_argument('--numprojects', type=int, default=0,
                        help='Number of projects to use')
    parser.add_argument('--project', action='append', dest='initprojects',
                        default=[],
                        help='Include project')
    parser.add_argument('--projectpath', default='projects', help=argparse.SUPPRESS)

    parser.add_argument('--cardset', type=argparse.FileType('r'),
                        help='File containing list of cards to use')
    parser.add_argument('--cardbase', action='append',
                        help='Include only cards from the specified base')
    parser.add_argument('--cardpath', default='cards',
                        help='Where to find card definitions')
    parser.add_argument('--artifactpath', default='artifacts', help=argparse.SUPPRESS)
    parser.add_argument('--boonpath', default='boons', help=argparse.SUPPRESS)
    parser.add_argument('--numstacks', default=10, help=argparse.SUPPRESS)
    parser.add_argument('--prosperity', default=False, action='store_true',
                        help='Use colonies and platinums')
    parser.add_argument('--bot', action='store_true', dest='bot',
                        default=False,
                        help='Bot Player')
    parser.add_argument('--quiet', action='store_true', dest='quiet',
                        default=False,
                        help="Supress a lot of output")
    namespace = parser.parse_args(args)
    return namespace


###############################################################################
def runGame(args):      # pragma: no cover
    """ TODO """
    cards = args['initcards']
    if args['cardset']:
        for line in args['cardset']:
            if line.startswith('--prosperity'):
                args['prosperity'] = True
                continue
            cards.append(line.strip())
    args['initcards'] = cards
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
def main():     # pragma: no cover
    """ Command line entry point """
    args = parse_cli_args()
    runGame(vars(args))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    main()

# EOF

#!/usr/bin/env python
import argparse
import glob
import imp
import os
import random
import sys
import uuid

from TextPlayer import TextPlayer
from BotPlayer import BotPlayer
from CardPile import CardPile
from EventPile import EventPile
from LandmarkPile import LandmarkPile
from BoonPile import BoonPile
from HexPile import HexPile
from StatePile import StatePile
from ArtifactPile import ArtifactPile
from ProjectPile import ProjectPile
from PlayArea import PlayArea
from Names import playerNames


###############################################################################
###############################################################################
###############################################################################
class Game(object):
    def __init__(self, **kwargs):
        self.parseArgs(**kwargs)

        self.players = {}
        self.cardpiles = {}
        self.states = {}
        self.artifacts = {}
        self.projects = {}
        self.events = {}
        self.landmarks = {}
        self.boons = []
        self.discarded_boons = []
        self.retained_boons = []
        self.hexes = []
        self.discarded_hexes = []
        self.trashpile = PlayArea([])
        self.gameover = False
        self.currentPlayer = None
        self.baseCards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']
        if self.prosperity:
            self.baseCards.append('Colony')
            self.baseCards.append('Platinum')
        self.cardmapping = self.getAvailableCardClasses()

    ###########################################################################
    def parseArgs(self, **args):
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
        self.eventpath = 'events'
        self.numevents = args['numevents'] if 'numevents' in args else 0

        self.landmarkcards = args['landmarkcards'] if 'landmarkcards' in args else []
        self.landmarkpath = args['landmarkpath'] if 'landmarkpath' in args else 'landmarks'
        self.numlandmarks = args['numlandmarks'] if 'numlandmarks' in args else 0

        self.numprojects = args['numprojects'] if 'numprojects' in args else 0
        self.projectpath = args['projectpath'] if 'projectpath' in args else 'projects'
        self.initprojects = args['initprojects'] if 'initprojects' in args else []

    ###########################################################################
    def startGame(self, playernames=[], plrKlass=TextPlayer):
        names = playerNames[:]
        self.loadDecks(self.initcards, self.numstacks)
        self.loadEvents()
        self.loadLandmarks()
        self.loadArtifacts()
        self.loadProjects()
        heirlooms = self.enable_heirlooms()

        if self.hexes or self.boons:
            self.loadStates()
        self.checkCardRequirements()

        for i in range(self.numplayers):
            try:
                name = playernames.pop()
            except IndexError:
                name = random.choice(names)
                names.remove(name)
            u = uuid.uuid4().hex
            if self.bot:
                self.players[u] = BotPlayer(game=self, quiet=self.quiet, name='%sBot' % name, heirlooms=heirlooms)
                self.bot = False
            else:
                self.players[u] = plrKlass(game=self, quiet=self.quiet, name=name, number=i, heirlooms=heirlooms)
            self.players[u].uuid = u
        self.cardSetup()
        self.numcards = self.countCards()
        self.currentPlayer = self.playerList(0)

    ###########################################################################
    def playerList(self, num=None):
        if num is None:
            return list(self.players.values())
        else:
            return list(self.players.values())[num]

    ###########################################################################
    def inTrash(self, cardname):
        """ Return named card if cardname is in the trash pile """
        if hasattr(cardname, 'name'):
            cardname = cardname.name
        for c in self.trashpile:
            if c.name == cardname:
                return c
        return None

    ###########################################################################
    def setTrash(self, *cards):
        """ This is mostly used for testing """
        self.trashpile.empty()
        for c in cards:
            self.trashpile.add(self[c].remove())

    ###########################################################################
    def cardSetup(self):
        """ Run the setup() method for all cards """
        for cp in list(self.cardpiles.values()):
            cp.setup(game=self)
        for lm in list(self.landmarks.values()):
            lm.setup(game=self)

    ###########################################################################
    def countCards(self):
        count = {}
        count['trash'] = self.trashSize()
        for cp in list(self.cardpiles.values()):
            count['pile_%s' % cp.name] = cp.numcards
        for pl in self.playerList():
            count['player_%s' % pl.name] = pl.countCards()
        total = sum([x for x in count.values()])
        return total

    ###########################################################################
    def output(self, msg):
        """ Send output to all players """
        if not self.quiet:
            sys.stdout.write("ALL: %s\n" % msg)

    ###########################################################################
    def trashSize(self):
        return len(self.trashpile)

    ###########################################################################
    def loadTravellers(self):
        travellers = self.getAvailableCards('Traveller')
        for trav in travellers:
            cp = CardPile(trav, self.cardmapping['Traveller'][trav], self)
            self.cardpiles[cp.name] = cp
        self.loaded_travellers = True

    ###########################################################################
    def loadEvents(self):
        self.loadNonKingdomCards('Event', self.eventcards, self.numevents, EventPile, self.events)

    ###########################################################################
    def loadLandmarks(self):
        self.loadNonKingdomCards('Landmark', self.landmarkcards, self.numlandmarks, LandmarkPile, self.landmarks)

    ###########################################################################
    def loadBoons(self):
        if self.boons:
            return
        self.output("Using boons")
        d = {}
        self.loadNonKingdomCards('Boon', None, None, BoonPile, d)
        self.boons = list(d.values())
        random.shuffle(self.boons)

    ###########################################################################
    def loadHexes(self):
        if self.hexes:
            return
        d = {}
        self.output("Using hexes")
        self.loadNonKingdomCards('Hex', None, None, HexPile, d)
        self.hexes = list(d.values())
        random.shuffle(self.hexes)

    ###########################################################################
    def loadStates(self):
        if self.states:
            return
        self.output("Using states")
        self.loadNonKingdomCards('State', None, None, StatePile, self.states)

    ###########################################################################
    def loadArtifacts(self):
        if self.artifacts:
            return
        self.output("Using artifacts")
        self.loadNonKingdomCards('Artifact', None, None, ArtifactPile, self.artifacts)

    ###########################################################################
    def loadProjects(self):
        if self.projects:
            return
        self.output("Using projects")
        self.loadNonKingdomCards('Project', self.initprojects, self.numprojects, ProjectPile, self.projects)

    ###########################################################################
    def loadNonKingdomCards(self, cardtype, specified, numspecified, cardKlass, dest):
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

        for l in dest:
            self.output("Playing with %s %s" % (cardtype, l))

    ###########################################################################
    def guess_cardname(self, name, prefix='Card'):
        """ Don't force the user to give the exact card name on the command
        line - maybe we can guess it """
        available = self.getAvailableCards(prefix)
        if name in available:
            return name
        for c in available:
            newc = c.replace("'", "")
            if newc.lower() == name.lower():
                return c
            newc = newc.replace(' ', '')
            if newc.lower() == name.lower():
                return c
        return None

    ###########################################################################
    def loadDecks(self, initcards, numstacks):
        for card in self.baseCards:
            cp = CardPile(card, self.cardmapping['BaseCard'][card], self)
            self.cardpiles[cp.name] = cp
        self['Copper'].numcards = 60
        self['Silver'].numcards = 40
        self['Gold'].numcards = 30
        available = self.getAvailableCards()
        unfilled = numstacks
        foundall = True
        for c in initcards:
            cardname = self.guess_cardname(c)
            if cardname:
                self.useCardPile(available, cardname, force=True)
                unfilled -= 1
                continue
            eventname = self.guess_cardname(c, 'Event')
            if eventname:
                self.eventcards.append(eventname)
                continue
            landmarkname = self.guess_cardname(c, 'Landmark')
            if landmarkname:
                self.landmarkcards.append(landmarkname)
                continue
            projectname = self.guess_cardname(c, 'Project')
            if projectname:
                self.initprojects.append(projectname)
                continue
            print("Can't guess what card '%s' is" % c)
            foundall = False
        if not foundall:
            sys.exit(1)

        while unfilled:
            c = random.choice(available)
            if c in self.badcards:
                continue
            unfilled -= self.useCardPile(available, c)

        self.checkCardRequirements()

    ###########################################################################
    def addPrizes(self):
        from PrizeCardPile import PrizeCardPile
        for prize in self.getAvailableCards('PrizeCard'):
            self.cardpiles[prize] = PrizeCardPile(prize, self.cardmapping['PrizeCard'][prize])
        self.output("Playing with Prizes")

    ###########################################################################
    def getPrizes(self):
        return list(self.cardmapping['PrizeCard'].keys())

    ###########################################################################
    def useCardPile(self, available, c, force=False):
        try:
            available.remove(c)
        except ValueError:  # pragma: no cover
            sys.stderr.write("Unknown card '%s'\n" % c)
            sys.exit(1)
        cp = CardPile(c, self.cardmapping['Card'][c], self)
        if not force and not cp.insupply:
            return 0
        self.cardpiles[cp.name] = cp
        self.output("Playing with card %s" % self[c].name)
        return 1

    ###########################################################################
    def enable_heirlooms(self):
        """ Go through the cardpiles and see if any require heirloom cards
        to be brought into the game """
        heirlooms = set()
        for card in list(self.cardpiles.values()):
            if card.heirloom is not None:
                heirlooms.add(card.heirloom)
                cp = CardPile(card.heirloom, self.cardmapping['Heirloom'][card.heirloom], self)
                self.cardpiles[cp.name] = cp

        return list(heirlooms)

    ###########################################################################
    def checkCardRequirements(self):
        for card in list(self.cardpiles.values()) + list(self.events.values()) + list(self.hexes) + list(self.boons):
            for x in card.required_cards:
                if isinstance(x, tuple):
                    k, c = x
                else:
                    k, c = 'BaseCard', x
                if c not in self.cardpiles:
                    self.cardpiles[c] = CardPile(c, self.cardmapping[k][c], self)
                    self.output("Playing with %s" % c)

        for card in self.landmarks.values():
            for x in card.required_cards:
                if isinstance(x, tuple):
                    k, c = x
                else:
                    k, c = 'BaseCard', x
                if c not in self.cardpiles:
                    self.cardpiles[c] = CardPile(c, self.cardmapping[k][c], self)
                    self.output("Playing with %s" % c)

        for card in list(self.cardpiles.keys()):
            if self.cardpiles[card].isLooter() and 'Ruins' not in self.cardpiles:
                from RuinCardPile import RuinCardPile
                nc = self.numplayers * 10
                self.cardpiles['Ruins'] = RuinCardPile(self.cardmapping['RuinCard'], numcards=nc)
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
        return list(self.cardpiles.values())

    ###########################################################################
    def __getitem__(self, key):
        return self.cardpiles[key]

    ###########################################################################
    def __contains__(self, key):
        return key in self.cardpiles

    ###########################################################################
    def getAvailableCardClasses(self):
        """ Create a mapping between the cardname and the module """
        mapping = {}
        for prefix in ('Card', 'Traveller', 'BaseCard', 'RuinCard', 'PrizeCard', 'KnightCard', 'Castle', 'Heirloom'):
            mapping[prefix] = self.getSetCardClasses(prefix, self.cardpath, 'cards', 'Card_')
        mapping['Event'] = self.getSetCardClasses('Event', self.eventpath, 'events', 'Event_')
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
        for fname in [os.path.basename(f) for f in files]:
            fname = fname.replace('.py', '')
            fp, pathname, desc = imp.find_module(fname, [path, defdir])
            mod = imp.load_module(fname, fp, pathname, desc)
            fp.close()
            classes = dir(mod)
            for c in classes:
                if c.startswith(class_prefix):
                    klass = getattr(mod, c)
                    break
            else:   # pragma: no cover
                sys.stderr.write("Couldn't find %s Class in %s\n" % (prefix, pathname))
            k = klass()
            mapping[k.name] = klass
        return mapping

    ###########################################################################
    def getAvailableCards(self, prefix='Card'):
        return list(self.cardmapping[prefix].keys())

    ###########################################################################
    def getActionPiles(self, cost=999):
        """ Return all cardstacks that are action cards that cost less than cost """
        actionpiles = []
        for cp in self.cardpiles.values():
            if not cp.purchasable:
                continue
            if cp.cost > cost:
                continue
            if cp.isAction():
                actionpiles.append(cp)
        return actionpiles

    ###########################################################################
    def getVictoryPiles(self):
        """ Return all cardstacks that are victory cards """
        victorypiles = []
        for cp in self.cardpiles.values():
            if cp.isVictory():
                victorypiles.append(cp)
        return victorypiles

    ###########################################################################
    def isGameOver(self):
        numEmpty = 0
        for c in self.cardpiles:
            if self[c].isEmpty():
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
        print("Trash: %s" % ", ".join([c.name for c in self.trashpile]))
        print("Boons: {}".format(", ".join([_.name for _ in self.boons])))
        print("Hexes: {}".format(", ".join([_.name for _ in self.hexes])))
        print("Projects: {}".format(", ".join([_.name for _ in self.projects.values()])))
        for cp in self.cardpiles:
            tokens = ""
            for p in self.playerList():
                tkns = p.which_token(cp)
                if tkns:
                    tokens += "%s[%s]" % (p.name, ",".join(tkns))

            print("CardPile %s: %d cards %s" % (cp, self.cardpiles[cp].numcards, tokens))
        for p in self.playerList():
            print("\n%s's state: %s" % (p.name, ", ".join([s.name for s in p.states])))
            print("  %s's artifacts: %s" % (p.name, ", ".join([c.name for c in p.artifacts])))
            print("  %s's projects: %s" % (p.name, ", ".join([c.name for c in p.projects])))
            print("  %s's hand: %s" % (p.name, ", ".join([c.name for c in p.hand])))
            print("  %s's deck: %s" % (p.name, ", ".join([c.name for c in p.deck])))
            print("  %s's discard: %s" % (p.name, ", ".join([c.name for c in p.discardpile])))
            print("  %s's duration: %s" % (p.name, ", ".join([c.name for c in p.durationpile])))
            print("  %s's reserve: %s" % (p.name, ", ".join([c.name for c in p.reserve])))
            print("  %s's played: %s" % (p.name, ", ".join([c.name for c in p.played])))
            print("  %s's messages: %s" % (p.name, p.messages))
            print("  %s's score: %s %s" % (p.name, p.getScore(), p.getScoreDetails()))
            print("  %s's tokens: %s" % (p.name, p.tokens))
            print("  %s's turn: coin=%d debt=%d actions=%d buys=%d coffers=%d villagers=%d potions=%d" % (p.name, p.coin, p.debt, p.actions, p.buys, p.coffer, p.villager, p.potions))

    ###########################################################################
    def playerToLeft(self, plr):
        """ Return the player to the 'left' of the one specified """
        players = self.playerList()
        place = players.index(plr) - 1
        return players[place]

    ###########################################################################
    def playerToRight(self, plr):
        """ Return the player to the 'right' of the one specified """
        players = self.playerList()
        place = (players.index(plr) + 1) % len(players)
        return players[place]

    ###########################################################################
    def whoWon(self):
        scores = {}
        self.output("")
        self.output("Scores:")
        for plr in self.playerList():
            scores[plr.name] = plr.getScore(verbose=True)
        self.output(scores)
        self.output("")
        for plr in self.playerList():
            self.output("Cards of %s:" % plr.name)
            for k, v in plr.getCards().items():
                self.output("%s: %s=%s" % (plr.name, k, v))
        self.output("Trash: %s" % ", ".join([c.name for c in self.trashpile]))
        return scores

    ###########################################################################
    def count_all_cards(self):  # pragma: no cover
        for pile in self.cardpiles.values():
            total = pile.numcards
            sys.stderr.write("%-15s  " % pile.name)
            if total:
                sys.stderr.write("pile=%d " % total)
            for plr in self.playerList():
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
        try:
            assert(self.countCards() == self.numcards)
        except AssertionError:
            self.count_all_cards()
            sys.stderr.write("current = %s\n" % self.countCards())
            sys.stderr.write("original = %d\n" % self.numcards)
            raise
        self.currentPlayer = self.playerToLeft(self.currentPlayer)
        self.currentPlayer.startTurn()
        self.currentPlayer.turn()
        self.currentPlayer.endTurn()
        if self.isGameOver():
            self.gameover = True
            for plr in self.playerList():
                plr.gameOver()


###############################################################################
def parseArgs(args=sys.argv[1:]):
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
    cards = args['initcards']
    if args['cardset']:
        for line in args['cardset']:
            cards.append(line.strip())
    args['initcards'] = cards
    g = Game(**args)
    g.startGame()
    try:
        while not g.gameover:
            try:
                g.turn()
            except Exception:
                g.print_state()
                raise
    except KeyboardInterrupt:
        g.gameover = True
        pass
    g.whoWon()


###############################################################################
def main():     # pragma: no cover
    args = parseArgs()
    runGame(vars(args))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    main()

# EOF

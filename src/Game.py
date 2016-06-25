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
        self.events = {}
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
        self.prosperity = False
        self.quiet = False
        self.numplayers = 2
        self.numevents = 0
        self.initcards = []
        self.badcards = []
        self.eventcards = []
        self.cardpath = 'cards'
        self.eventpath = 'events'
        self.cardbase = []
        self.bot = False
        if 'prosperity' in args:
            self.prosperity = args['prosperity']
        if 'quiet' in args:
            self.quiet = args['quiet']
        if 'numplayers' in args:
            self.numplayers = args['numplayers']
        if 'numevents' in args:
            self.numevents = args['numevents']
        if 'initcards' in args:
            self.initcards = args['initcards']
        if 'badcards' in args:
            self.badcards = args['badcards']
        if 'eventcards' in args:
            self.eventcards = args['eventcards']
        if 'cardpath' in args:
            self.cardpath = args['cardpath']
        if 'cardbase' in args:
            self.cardbase = args['cardbase']
        if 'bot' in args:
            self.bot = args['bot']

    ###########################################################################
    def startGame(self, playernames=[], plrKlass=TextPlayer):
        names = playerNames[:]
        self.loadDecks(self.initcards)
        self.loadEvents()

        for c in list(self.cardpiles.keys()):
            self.checkCardRequirements(c)

        for i in range(self.numplayers):
            try:
                name = playernames.pop()
            except IndexError:
                name = random.choice(names)
                names.remove(name)
            u = uuid.uuid4().hex
            if self.bot:
                self.players[u] = BotPlayer(game=self, quiet=self.quiet, name='%sBot' % name)
                self.bot = False
            else:
                self.players[u] = plrKlass(game=self, quiet=self.quiet, name=name, number=i)
            self.players[u].uuid = u
        self.numcards = self.countCards()
        self.cardSetup()
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
        available = self.getAvailableCards('Event')
        # Specified Events
        for ev in self.eventcards:
            try:
                evklass = self.cardmapping['Event'][ev]
                self.events[ev] = EventPile(ev, evklass)
                available.remove(ev)
            except (ValueError, KeyError):
                sys.stderr.write("Unknown event '%s'\n" % ev)
                sys.exit(1)
        # Events to make up the numbers
        while len(self.events) < self.numevents:
            ev = random.choice(available)
            evklass = self.cardmapping['Event'][ev]
            self.events[ev] = EventPile(ev, evklass)
            available.remove(ev)
        for e in self.events:
            self.output("Playing with event %s" % e)

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
    def loadDecks(self, initcards):
        for card in self.baseCards:
            cp = CardPile(card, self.cardmapping['BaseCard'][card], self)
            self.cardpiles[cp.name] = cp
        self['Copper'].numcards = 60
        self['Silver'].numcards = 40
        self['Gold'].numcards = 30
        available = self.getAvailableCards()
        unfilled = 10
        foundall = True
        for c in initcards:
            cardname = self.guess_cardname(c)
            if cardname:
                self.useCardPile(available, cardname)
                unfilled -= 1
                continue
            eventname = self.guess_cardname(c, 'Event')
            if eventname:
                self.eventcards.append(eventname)
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

        for c in list(self.cardpiles.keys()):
            self.checkCardRequirements(c)

    ###########################################################################
    def numCurses(self):
        # The max here is to help for testing in 1 player games
        # so the number of curses is never 0
        return max(10, 10 * (self.numplayers - 1))

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
    def addKnights(self):
        from KnightCardPile import KnightCardPile
        self.cardpiles['Knights'] = KnightCardPile(cardpath=self.cardpath)

    ###########################################################################
    def useCardPile(self, available, c):
        try:
            available.remove(c)
        except ValueError:  # pragma: no cover
            sys.stderr.write("Unknown card '%s'\n" % c)
            sys.exit(1)
        cp = CardPile(c, self.cardmapping['Card'][c], self)
        self.cardpiles[cp.name] = cp
        self.output("Playing with card %s" % self[c].name)
        return 1

    ###########################################################################
    def checkCardRequirements(self, card):
        if self.cardpiles[card].needcurse and 'Curse' not in self.cardpiles:
            self.cardpiles['Curse'] = CardPile('Curse', self.cardmapping['BaseCard']['Curse'], numcards=self.numCurses())
            self.output("Playing with Curses")
        if self.cardpiles[card].potcost and 'Potion' not in self.cardpiles:
            self.cardpiles['Potion'] = CardPile('Potion', self.cardmapping['BaseCard']['Potion'], numcards=16)
            self.output("Playing with Potions")
        if self.cardpiles[card].isLooter() and 'Ruins' not in self.cardpiles:
            from RuinCardPile import RuinCardPile
            nc = self.numplayers * 10
            self.cardpiles['Ruins'] = RuinCardPile(self.cardmapping['RuinCard'], numcards=nc)
            self.output("Playing with Ruins")
        if self.cardpiles[card].needspoils and 'Spoils' not in self.cardpiles:
            self.cardpiles['Spoils'] = CardPile('Spoils', self.cardmapping['BaseCard']['Spoils'], numcards=16)
            self.output("Playing with Spoils")
        if self.cardpiles[card].traveller:
            self.loadTravellers()
        if self.cardpiles[card].needsmadman and 'Madman' not in self.cardpiles:
            self.cardpiles['Madman'] = CardPile('Madman', self.cardmapping['BaseCard']['Madman'], numcards=10)
            self.output("Playing with Madman")
        if self.cardpiles[card].needsmercenary and 'Mercenary' not in self.cardpiles:
            self.cardpiles['Mercenary'] = CardPile('Mercenary', self.cardmapping['BaseCard']['Mercenary'], numcards=10)
            self.output("Playing with Mercenary")
        if self.cardpiles[card].needsprize:
            self.addPrizes()

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
        for prefix in ('Card', 'Traveller', 'BaseCard', 'RuinCard', 'PrizeCard', 'KnightCard'):
            mapping[prefix] = self.getSetCardClasses(prefix, self.cardpath, 'cards', 'Card_')
        mapping['Event'] = self.getSetCardClasses('Event', self.eventpath, 'events', 'Event_')
        return mapping

    ###########################################################################
    def getSetCardClasses(self, prefix, path, defdir, class_prefix):
        """ Import all the modules to determine the real name of the card
            This is slow, but it is the only way """
        mapping = {}
        files = glob.glob('%s/%s_*.py' % (path, prefix))
        for fname in [os.path.basename(f) for f in files]:
            fname = fname.replace('.py', '')
            fp, pathname, desc = imp.find_module(fname, [path, defdir])
            mod = imp.load_module(fname, fp, pathname, desc)
            classes = dir(mod)
            for c in classes:
                if c.startswith(class_prefix):
                    klass = getattr(mod, c)
                    break
            else:
                sys.stderr.write("Couldn't find %s Class in %s\n" % (prefix, pathname))
            k = klass()
            mapping[k.name] = klass
        return mapping

    ###########################################################################
    def getAvailableCards(self, prefix='Card'):
        return list(self.cardmapping[prefix].keys())

    ###########################################################################
    def getActionPiles(self):
        """ Return all cardstacks that are action cards """
        actionpiles = []
        for cp in self.cardpiles.values():
            if not cp.purchasable:
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
    def print_state(self):  # pragma: no cover
        """ This is used for debugging """
        print("#" * 40)
        print("Trash: %s" % ", ".join([c.name for c in self.trashpile]))
        for cp in self.cardpiles:
            tokens = ""
            for p in self.playerList():
                tkns = p.which_token(cp)
                if tkns:
                    tokens += "%s[%s]" % (p.name, ",".join(tkns))

            print("CardPile %s: %d cards %s" % (cp, self.cardpiles[cp].numcards, tokens))
        for p in self.playerList():
            print("%s's hand: %s" % (p.name, ", ".join([c.name for c in p.hand])))
            print("%s's deck: %s" % (p.name, ", ".join([c.name for c in p.deck])))
            print("%s's discard: %s" % (p.name, ", ".join([c.name for c in p.discardpile])))
            print("%s's duration: %s" % (p.name, ", ".join([c.name for c in p.durationpile])))
            print("%s's reserve: %s" % (p.name, ", ".join([c.name for c in p.reserve])))
            print("%s's played: %s" % (p.name, ", ".join([c.name for c in p.played])))
            print("%s's messages: %s" % (p.name, p.messages))
            print("%s's score: %s" % (p.name, p.score))
            print("%s's tokens: %s" % (p.name, p.tokens))
            print("%s's turn: coin=%d actions=%d buys=%d special coins=%d potions=%d" % (p.name, p.coin, p.actions, p.buys, p.specialcoins, p.potions))
        cpls = ["%s=%s" % (name, cp.numcards) for name, cp in self.cardpiles.items()]
        print("%s" % ", ".join(cpls))

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
    parser.add_argument('--event', action='append', dest='eventcards',
                        default=[],
                        help='Include event')
    parser.add_argument('--numevents', type=int, default=0,
                        help='Number of events to use')
    parser.add_argument('--cardset', type=argparse.FileType('r'),
                        help='File containing list of cards to use')
    parser.add_argument('--cardbase', action='append',
                        help='Include only cards from the specified base')
    parser.add_argument('--cardpath', default='cards',
                        help='Where to find card definitions')
    parser.add_argument('--prosperity', default=False, action='store_true',
                        help='Use colonies and platinums')
    parser.add_argument('--bot', action='store_true', dest='bot',
                        default=False,
                        help='Bot Player')
    namespace = parser.parse_args(args)
    return namespace


###############################################################################
def runGame(args):
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
def main():
    args = parseArgs()
    runGame(vars(args))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    main()

# EOF

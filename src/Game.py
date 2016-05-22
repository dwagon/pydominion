#!/usr/bin/env python
import argparse
import glob
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

    ###########################################################################
    def parseArgs(self, **args):
        self.prosperity = False
        self.quiet = False
        self.numplayers = 2
        self.numevents = 0
        self.initcards = []
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
        if self.needtravellers:
            self.loadTravellers()
        self.loadEvents()
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
            if c.cardname.lower() == cardname.lower():
                return c
        return None

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
            self.cardpiles[trav] = CardPile(trav, cardpath=self.cardpath, numcards=5)

    ###########################################################################
    def loadEvents(self):
        for ev in self.eventcards:
            evname = ev.title()
            self.events[evname] = EventPile(evname, eventpath=self.eventpath)
        available = self.getAvailableEvents()
        while len(self.events) < self.numevents:
            c = random.choice(available)
            if c not in self.events:
                self.events[c] = EventPile(c, eventpath=self.eventpath)
        for e in self.events:
            self.output("Playing with event %s" % e)

    ###########################################################################
    def loadDecks(self, initcards):
        for card in self.baseCards:
            self.cardpiles[card] = CardPile(card, numcards=12, cardpath=self.cardpath)
        self['Copper'].numcards = 60
        self['Silver'].numcards = 40
        self['Gold'].numcards = 30
        available = self.getAvailableCards()
        unfilled = 10 - len(initcards)
        self.needcurse = False
        self.needspoils = False
        self.needpotion = False
        self.needruins = False
        self.needtravellers = False
        for c in initcards:
            c = c.strip().lower().title()
            if c not in available:
                sys.stderr.write("Card '%s' is not available\n" % c)
                sys.exit(1)
            self.useCardPile(available, c)

        while unfilled:
            c = random.choice(available)
            unfilled -= self.useCardPile(available, c)
        if self.needcurse:
            self.cardpiles['Curse'] = CardPile('Curse', numcards=self.numCurses(), cardpath=self.cardpath)
            self.output("Playing with Curses")
        if self.needpotion:
            self.cardpiles['Potion'] = CardPile('Potion', numcards=16, cardpath=self.cardpath)
            self.output("Playing with Potions")
        if self.needspoils:
            self.cardpiles['Spoils'] = CardPile('Spoils', numcards=16, cardpath=self.cardpath)
            self.output("Playing with Spoils")
        if self.needruins:
            self.addRuins()

    ###########################################################################
    def numCurses(self):
        # The max here is to help for testing in 1 player games
        # so the number of curses is never 0
        return max(10, 10 * (self.numplayers - 1))

    ###########################################################################
    def addRuins(self):
        from RuinCardPile import RuinCardPile
        nc = self.numplayers * 10
        self.cardpiles['Ruins'] = RuinCardPile(cardpath=self.cardpath, numcards=nc)
        self.output("Playing with Ruins")

    ###########################################################################
    def addKnights(self):
        from KnightCardPile import KnightCardPile
        self.cardpiles['Knights'] = KnightCardPile(cardpath=self.cardpath)

    ###########################################################################
    def useCardPile(self, available, c):
        if self.cardbase:
            cp = CardPile(c, cardpath=self.cardpath, numcards=c.stacksize)
            if cp.base not in self.cardbase:
                return 0
        available.remove(c)
        self.cardpiles[c] = CardPile(c, cardpath=self.cardpath)
        self.output("Playing with card %s" % self[c].name)
        if self.cardpiles[c].needcurse:
            self.needcurse = True
        if self.cardpiles[c].potcost:
            self.needpotion = True
        if self.cardpiles[c].isLooter():
            self.needruins = True
        if self.cardpiles[c].needspoils:
            self.needspoils = True
        if self.cardpiles[c].traveller:
            self.needtravellers = True
        return 1

    ###########################################################################
    def cardTypes(self):
        return list(self.cardpiles.values())

    ###########################################################################
    def __getitem__(self, key):
        key = key.lower().title()
        return self.cardpiles[key]

    ###########################################################################
    def getAvailableCards(self, prefix='Card'):
        cardfiles = glob.glob('%s/%s_*.py' % (self.cardpath, prefix))
        cards = [c.replace('%s/%s_' % (self.cardpath, prefix), '').replace('.py', '') for c in cardfiles]
        return cards

    ###########################################################################
    def getAvailableEvents(self):
        eventfiles = glob.glob('%s/Event_*.py' % self.eventpath)
        events = [c.replace('%s/Event_' % self.eventpath, '').replace('.py', '') for c in eventfiles]
        return events

    ###########################################################################
    def getActionPiles(self):
        """ Return all cardstacks that are action cards """
        actionpiles = []
        for cp in self.cardpiles.values():
            if cp.isAction():
                actionpiles.append(cp)
        return actionpiles

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
        for plr in self.playerList():
            scores[plr.name] = plr.getScore(verbose=True)
        self.output(scores)
        return scores

    ###########################################################################
    def count_all_cards(self):
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


###############################################################################
def parseArgs(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Play dominion')
    parser.add_argument('--numplayers', type=int, default=2,
                        help='How many players')
    parser.add_argument('--card', action='append', dest='initcards',
                        default=[],
                        help='Include card in lineup')
    parser.add_argument('--event', action='append', dest='eventcards',
                        default=[],
                        help='Include event')
    parser.add_argument('--numevents', type=int, default=2,
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
            g.turn()
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

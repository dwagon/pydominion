#!/usr/bin/env python
import argparse
import glob
import random
import sys

from Player import Player
from CardPile import CardPile


###############################################################################
###############################################################################
###############################################################################
class Game(object):
    def __init__(self, quiet=False, prosperity=False):
        self.players = []
        self.cardpiles = {}
        self.trashpile = []
        self.gameover = False
        self.quiet = quiet
        self.prosperity = prosperity
        self.baseCards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']
        if self.prosperity:
            self.baseCards.append('Colony')
            self.baseCards.append('Platinum')

    ###########################################################################
    def startGame(self, numplayers, initcards=[], cardpath='cards', cardbase=[], playernames=[]):
        self.cardbase = cardbase
        self.cardpath = cardpath
        self.numplayers = numplayers
        self.loadDecks(initcards)
        for i in range(numplayers):
            try:
                name = playernames.pop()
            except IndexError:
                name = None
            self.players.append(Player(game=self, quiet=self.quiet, name=name))
        self.numcards = self.countCards()
        self.cardSetup()

    ###########################################################################
    def cardSetup(self):
        """ Run the setup() method for all cards """
        for cp in self.cardpiles.values():
            cp.setup(game=self)

    ###########################################################################
    def countCards(self):
        count = 0
        count += len(self.trashpile)
        for cp in self.cardpiles.values():
            count += cp.numcards
        for pl in self.players:
            count += pl.countCards()
        return count

    ###########################################################################
    def output(self, msg):
        """ Send output to all players """
        if not self.quiet:
            sys.stdout.write("ALL: %s\n" % msg)

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
            self.output("Playing with Curse")
        if self.needpotion:
            self.cardpiles['Potion'] = CardPile('Potion', numcards=16, cardpath=self.cardpath)
            self.output("Playing with Potion")
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
        self.cardpiles['Ruins'] = RuinCardPile(cardpath=self.cardpath, numcards=self.numCurses())
        self.output("Playing with Ruins")

    ###########################################################################
    def addKnights(self):
        from KnightCardPile import KnightCardPile
        self.cardpiles['Knights'] = KnightCardPile(cardpath=self.cardpath)

    ###########################################################################
    def useCardPile(self, available, c):
        if self.cardbase:
            cp = CardPile(c, cardpath=self.cardpath)
            if cp.base not in self.cardbase:
                return 0
        available.remove(c)
        self.cardpiles[c] = CardPile(c, cardpath=self.cardpath)
        self.output("Playing with %s" % self[c].name)
        if self.cardpiles[c].needcurse:
            self.needcurse = True
        if self.cardpiles[c].potcost:
            self.needpotion = True
        if self.cardpiles[c].isLooter():
            self.needruins = True
        if self.cardpiles[c].needspoils:
            self.needspoils = True
        return 1

    ###########################################################################
    def cardTypes(self):
        return list(self.cardpiles.values())

    ###########################################################################
    def __getitem__(self, key):
        key = key.lower().title()
        return self.cardpiles[key]

    ###########################################################################
    def getAvailableCards(self):
        cardfiles = glob.glob('%s/Card_*.py' % self.cardpath)
        cards = [c.replace('%s/Card_' % self.cardpath, '').replace('.py', '') for c in cardfiles]
        return cards

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
    def print_state(self):
        """ This is used for debugging """
        print "#" * 40
        print "Trash: %s" % ", ".join([c.name for c in self.trashpile])
        for p in self.players:
            print "%s's hand: %s" % (p.name, ", ".join([c.name for c in p.hand]))
            print "%s's deck: %s" % (p.name, ", ".join([c.name for c in p.deck]))
            print "%s's discard: %s" % (p.name, ", ".join([c.name for c in p.discardpile]))
            print "%s's played: %s" % (p.name, ", ".join([c.name for c in p.played]))
            print "%s's messages: %s" % (p.name, p.messages)
            print "%s's score: %s" % (p.name, p.score)
            print "%s's turn: %s" % (p.name, p.t)
        cpls = ["%s=%s" % (name, cp.numcards) for name, cp in self.cardpiles.items()]
        print "%s" % ", ".join(cpls)

    ###########################################################################
    def playerToLeft(self, plr):
        """ Return the player to the 'left' of the one specified """
        place = self.players.index(plr) - 1
        return self.players[place]

    ###########################################################################
    def whoWon(self):
        scores = {}
        self.output("")
        for plr in self.players:
            scores[plr.name] = plr.getScore(verbose=True)
        self.output(scores)

    ###########################################################################
    def turn(self):
        assert(self.countCards() == self.numcards)
        for plr in self.players:
            plr.turn()
            if self.isGameOver():
                self.gameover = True
                break


###############################################################################
def parseArgs():
    parser = argparse.ArgumentParser(description='Play dominion')
    parser.add_argument('--numplayers', type=int, default=2,
                        help='How many players')
    parser.add_argument('--card', action='append', dest='initcards',
                        default=[],
                        help='Include card in lineup')
    parser.add_argument('--cardset', type=argparse.FileType('r'),
                        help='File containing list of cards to use')
    parser.add_argument('--cardbase', action='append',
                        help='Include only cards from the specified base')
    parser.add_argument('--cardpath', default='cards',
                        help='Where to find card definitions')
    parser.add_argument('--prosperity', default=False, action='store_true',
                        help='Use colonies and platinums')
    args = parser.parse_args()
    return args


###############################################################################
def runGame(args):
    cards = args.initcards
    if args.cardset:
        for line in args.cardset:
            cards.append(line.strip())
    g = Game(prosperity=args.prosperity)
    g.startGame(numplayers=args.numplayers, initcards=cards,
                cardpath=args.cardpath, cardbase=args.cardbase)
    try:
        while not g.gameover:
            g.turn()
    except KeyboardInterrupt:
        pass
    g.whoWon()


###############################################################################
def main():
    args = parseArgs()
    runGame(args)


###############################################################################
if __name__ == "__main__":
    main()

#EOF

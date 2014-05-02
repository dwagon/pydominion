#!/usr/bin/env python
import glob
import random
import sys

from Player import Player
from CardPile import CardPile


###############################################################################
###############################################################################
###############################################################################
class Game(object):
    def __init__(self, prosperity=False):
        self.players = []
        self.cardpiles = {}
        self.trashpile = []
        self.gameover = False
        self.prosperity = prosperity
        self.baseCards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']
        if self.prosperity:
            self.baseCards.append('Colony')
            self.baseCards.append('Platinum')

    ###########################################################################
    def startGame(self, numplayers, initcards=[], cardpath='cards', cardbase=[]):
        self.cardbase = cardbase
        self.cardpath = cardpath
        self.loadDecks(initcards, numplayers)
        for i in range(numplayers):
            self.players.append(Player(game=self))

    ###########################################################################
    def output(self, msg):
        """ Send output to all players """
        sys.stdout.write("ALL: %s\n" % msg)

    ###########################################################################
    def loadDecks(self, initcards, numplayers):
        for card in self.baseCards:
            self.cardpiles[card] = CardPile(card, numcards=12, cardpath=self.cardpath)
        self['Copper'].numcards = 60
        self['Silver'].numcards = 40
        self['Gold'].numcards = 30
        available = self.getAvailableCards()
        unfilled = 10 - len(initcards)
        self.needcurse = False
        self.needpotion = False
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
            self.cardpiles['Curse'] = CardPile('Curse', numcards=10*(numplayers-1), cardpath=self.cardpath)
            self.output("Playing with Curse")
        if self.needpotion:
            self.cardpiles['Potion'] = CardPile('Potion', numcards=16, cardpath=self.cardpath)
            self.output("Playing with Potion")

    ###########################################################################
    def useCardPile(self, available, c):
        cp = CardPile(c, cardpath=self.cardpath)
        if not self.cardbase or cp.base in self.cardbase:
            return 0
        self.output("Playing with %s" % c)
        available.remove(c)
        self.cardpiles[c] = CardPile(c, cardpath=self.cardpath)
        if self.cardpiles[c].needcurse:
            self.needcurse = True
        if self.cardpiles[c].potcost:
            self.needpotion = True
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
    def playerToLeft(self, plr):
        """ Return the player to the 'left' of the one specified """
        place = self.players.index(plr) - 1
        return self.players[place]

    ###########################################################################
    def whoWon(self):
        scores = {}
        for plr in self.players:
            scores[plr.name] = plr.score(verbose=True)
        self.output(scores)

    ###########################################################################
    def turn(self):
        for plr in self.players:
            plr.turn()
        if self.isGameOver():
            self.gameover = True


###############################################################################
def parseArgs():
    import argparse
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
    g.startGame(numplayers=args.numplayers, initcards=cards, cardpath=args.cardpath, cardbase=args.cardbase)
    while not g.gameover:
        g.turn()
    g.whoWon()


###############################################################################
def main():
    args = parseArgs()
    runGame(args)


###############################################################################
if __name__ == "__main__":
    main()

#EOF

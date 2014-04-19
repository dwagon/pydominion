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
    def __init__(self):
        self.players = []
        self.cardpiles = {}
        self.trashpile = []
        self.gameover = False
        self.baseCards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']

    ###########################################################################
    def startGame(self, numplayers, initcards=[]):
        self.loadDecks(initcards, numplayers)
        for i in range(numplayers):
            self.players.append(Player(game=self))

    ###########################################################################
    def loadDecks(self, initcards, numplayers):
        for card in self.baseCards:
            self.cardpiles[card] = CardPile(card, numcards=12)
        self['Copper'].numcards = 60
        self['Silver'].numcards = 40
        self['Gold'].numcards = 30
        available = self.getAvailableCards()
        unfilled = 10 - len(initcards)
        self.needcurse = False
        for c in initcards:
            c = c.strip().lower().title()
            if c not in available:
                sys.stderr.write("Card '%s' is not available\n" % c)
                sys.exit(1)
            self.useCardPile(available, c)

        while unfilled:
            c = random.choice(available)
            self.useCardPile(available, c)
            unfilled -= 1
        if self.needcurse:
            self.cardpiles['Curse'] = CardPile('Curse', numcards=10*(numplayers-1))

    ###########################################################################
    def useCardPile(self, available, c):
        sys.stderr.write("Playing with %s\n" % c)
        available.remove(c)
        self.cardpiles[c] = CardPile(c)
        if self.cardpiles[c].needcurse:
            self.needcurse = True

    ###########################################################################
    def cardsUnder(self, cost):
        """Return the list of cards for under $cost """
        purchbase = [c for c in self.cardTypes() if c.cost <= cost and c.numcards and c.basecard]
        purchnorm = [c for c in self.cardTypes() if c.cost <= cost and c.numcards and not c.basecard]
        purchbase.sort(key=lambda c: c.cost)
        purchnorm.sort(key=lambda c: c.cost)
        return purchnorm + purchbase

    ###########################################################################
    def cardTypes(self):
        return self.cardpiles.values()

    ###########################################################################
    def __getitem__(self, key):
        key = key.lower().title()
        return self.cardpiles[key]

    ###########################################################################
    def getAvailableCards(self):
        cardfiles = glob.glob('cards/Card_*.py')
        cards = [c.replace('cards/Card_', '').replace('.py', '') for c in cardfiles]
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
    def whoWon(self):
        scores = {}
        for plr in self.players:
            scores[plr.name] = plr.score()
        print scores

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
    args = parser.parse_args()
    return args


###############################################################################
def runGame(args):
    cards = args.initcards
    if args.cardset:
        for line in args.cardset:
            cards.append(line.strip())
    g = Game()
    g.startGame(numplayers=args.numplayers, initcards=cards)
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

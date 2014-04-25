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
    def startGame(self, numplayers, initcards=[], cardpath='cards'):
        self.loadDecks(initcards, numplayers, cardpath)
        for i in range(numplayers):
            self.players.append(Player(game=self))

    ###########################################################################
    def loadDecks(self, initcards, numplayers, cardpath):
        for card in self.baseCards:
            self.cardpiles[card] = CardPile(card, numcards=12, cardpath=cardpath)
        self['Copper'].numcards = 60
        self['Silver'].numcards = 40
        self['Gold'].numcards = 30
        available = self.getAvailableCards(cardpath)
        unfilled = 10 - len(initcards)
        self.needcurse = False
        for c in initcards:
            c = c.strip().lower().title()
            if c not in available:
                sys.stderr.write("Card '%s' is not available\n" % c)
                sys.exit(1)
            self.useCardPile(available, c, cardpath)

        while unfilled:
            c = random.choice(available)
            self.useCardPile(available, c, cardpath)
            unfilled -= 1
        if self.needcurse:
            self.cardpiles['Curse'] = CardPile('Curse', numcards=10*(numplayers-1), cardpath=cardpath)

    ###########################################################################
    def useCardPile(self, available, c, cardpath):
        sys.stderr.write("Playing with %s\n" % c)
        available.remove(c)
        self.cardpiles[c] = CardPile(c, cardpath=cardpath)
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
    def cardsWorth(self, cost):
        """Return the list of cards that are exactly $cost """
        purchbase = [c for c in self.cardTypes() if c.cost == cost and c.numcards and c.basecard]
        purchnorm = [c for c in self.cardTypes() if c.cost == cost and c.numcards and not c.basecard]
        purchbase.sort(key=lambda c: c.cost)
        purchnorm.sort(key=lambda c: c.cost)
        return purchnorm + purchbase

    ###########################################################################
    def cardTypes(self):
        return list(self.cardpiles.values())

    ###########################################################################
    def __getitem__(self, key):
        key = key.lower().title()
        return self.cardpiles[key]

    ###########################################################################
    def getAvailableCards(self, cardpath):
        cardfiles = glob.glob('%s/Card_*.py' % cardpath)
        cards = [c.replace('%s/Card_' % cardpath, '').replace('.py', '') for c in cardfiles]
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
            scores[plr.name] = plr.score()
        print(scores)

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
    parser.add_argument('--cardpath', default='cards',
                        help='Where to find card definitions')
    args = parser.parse_args()
    return args


###############################################################################
def runGame(args):
    cards = args.initcards
    if args.cardset:
        for line in args.cardset:
            cards.append(line.strip())
    g = Game()
    g.startGame(numplayers=args.numplayers, initcards=cards, cardpath=args.cardpath)
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

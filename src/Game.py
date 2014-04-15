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
    def startGame(self, numplayers):
        self.loadDecks()
        for i in range(numplayers):
            self.players.append(Player(game=self))

    ###########################################################################
    def loadDecks(self):
        for card in self.baseCards:
            self.cardpiles[card] = CardPile(card, numcards=50)
        available = self.getAvailableCards()
        unfilled = 10
        needcurse = False
        while unfilled:
            c = random.choice(available)
            sys.stderr.write("Playing with %s\n" % c)
            available.remove(c)
            self.cardpiles[c] = CardPile(c)
            if self.cardpiles[c].needcurse:
                needcurse = True
            unfilled -= 1
        if needcurse:
            self.cardpiles['Curse'] = CardPile('Curse', numcards=50)

    ###########################################################################
    def cardsUnder(self, cost):
        """Return the list of cards for under $cost """
        purchasable = [c for c in self.cardTypes() if c.cost <= cost and c.numcards]
        purchasable.sort(key=lambda c: c.cost)
        purchasable.sort(key=lambda c: c.cardtype)
        return purchasable

    ###########################################################################
    def cardTypes(self):
        return self.cardpiles.values()

    ###########################################################################
    def __getitem__(self, key):
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
    def turn(self):
        for plr in self.players:
            plr.turn()
        if self.isGameOver():
            self.gameover = True

###############################################################################
if __name__ == "__main__":
    g = Game()
    g.startGame(numplayers=2)
    while not g.gameover:
        g.turn()

#EOF

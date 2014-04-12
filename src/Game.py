#!/usr/bin/env python
import glob
import random
import sys

from Player import Player
from CardPile import CardPile

baseCards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province']

class Game(object):
    def __init__(self):
        self.players = []
        self.cardpiles = {}
        self.gameover = False

    def startGame(self, numplayers):
        self.loadDecks()
        for i in range(numplayers):
            self.players.append(Player(game=self))

    def loadDecks(self):
        for card in baseCards:
            self.cardpiles[card] = CardPile(card, numcards=50)
        available = self.getAvailableCards()
        unfilled = 10
        while unfilled:
            c = random.choice(available)
            sys.stderr.write("Playing with %s\n" % c)
            available.remove(c)
            self.cardpiles[c] = CardPile(c)
            unfilled -= 1

    def getAvailableCards(self):
        cardfiles = glob.glob('cards/Card_*.py')
        cards = [c.replace('cards/Card_', '').replace('.py', '') for c in cardfiles]
        return cards

    def turn(self):
        for plr in self.players:
            plr.turn()


if __name__ == "__main__":
    g = Game()
    g.startGame(numplayers=2)
    while not g.gameover:
        g.turn()
        for p in g.players:
            print repr(p)

#EOF

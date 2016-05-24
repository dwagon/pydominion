#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Merchantship(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'seaside'
        self.desc = "+2 coins; +2 coins next turn"
        self.name = 'Merchant Ship'
        self.coin = 2
        self.cost = 5

    def duration(self, game, player):
        """ Now and at the start of your next turn +2 coins """
        player.output("2 more coins from Merchant Ship")
        player.addCoin(2)


###############################################################################
class Test_Merchantship(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Merchant Ship'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Merchant Ship'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a merchant ship """
        self.plr.playCard(self.card)
        self.assertEquals(self.plr.getCoin(), 2)
        self.assertEquals(self.plr.durationSize(), 1)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEquals(self.plr.durationSize(), 0)
        self.assertEquals(self.plr.getCoin(), 2)
        self.assertEquals(self.plr.playedSize(), 1)
        self.assertEquals(self.plr.played[-1].name, 'Merchant Ship')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

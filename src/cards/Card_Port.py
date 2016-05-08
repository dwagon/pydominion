#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Port(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'adventure'
        self.desc = "+1 Card, +2 Actions; When you buy this, gain another Port"
        self.name = 'Port'
        self.cards = 1
        self.actions = 2
        self.cost = 4
        self.stacksize = 12

    def hook_buyThisCard(self, game, player):
        """ Gain another Port"""
        c = player.gainCard('port')
        if c:
            player.output("Gained a port")
        else:
            player.output("No more ports")


###############################################################################
class Test_Port(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['port'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['port'].remove()

    def test_play(self):
        """ Play a port """
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertEqual(self.plr.getActions(), 2)

    def test_buy(self):
        """ Buy a port """
        self.plr.setDiscard()
        self.plr.buyCard('port')
        for c in self.plr.discardpile:
            self.assertEqual(c.name, 'Port')
        self.assertEqual(self.plr.discardSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

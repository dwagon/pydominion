#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Bordervillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.desc = "+1 card, +2 action. When you gain this, gain a card costing less than this"
        self.name = 'Border Village'
        self.cost = 6
        self.cards = 1
        self.actions = 2

    def hook_gainThisCard(self, game, player):
        """ When you gain this, gain a card costing less than this"""
        newcost = self.cost - 1
        player.output("Gain a card costing %d due to Border Village" % newcost)
        player.plrGainCard(cost=newcost)


###############################################################################
class Test_Bordervillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Border Village'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.bv = self.g['Border Village'].remove()
        self.plr.addCard(self.bv, 'hand')

    def test_play(self):
        self.plr.playCard(self.bv)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 6)

    def test_gain(self):
        self.plr.test_input = ['get estate']
        self.plr.gainCard('Border Village')
        self.assertEqual(self.plr.discardSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

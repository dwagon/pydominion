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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['bordervillage'])
        self.plr = self.g.players[0]
        self.bv = self.g['bordervillage'].remove()
        self.plr.addCard(self.bv, 'hand')

    def test_play(self):
        self.plr.playCard(self.bv)
        self.assertEqual(self.plr.t['actions'], 2)
        self.assertEqual(len(self.plr.hand), 6)

    def test_gain(self):
        self.plr.test_input = ['4']
        self.plr.gainCard('bordervillage')
        self.assertEqual(len(self.plr.discardpile), 2)


###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF

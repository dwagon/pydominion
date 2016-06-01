#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Transmogrify(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reserve']
        self.base = 'adventure'
        self.desc = """+1 Action; At the start of your turn, you may call this,
        to trash a card from your hand, gain a card costing up to 1 coin more
        than it, and put that card intro your hand"""
        self.name = 'Transmogrify'
        self.actions = 1
        self.when = 'start'
        self.cost = 4

    def hook_callReserve(self, game, player):
        player.output("Trash a card from you hand. Gain a card costing up to 1 more")
        tc = player.plrTrashCard(printcost=True)
        if tc:
            cost = player.cardCost(tc[0])
            player.plrGainCard(cost+1, modifier='less', destination='hand')


###############################################################################
class Test_Transmogrify(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Transmogrify'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.trans = self.g['Transmogrify'].remove()
        self.plr.addCard(self.trans, 'hand')

    def test_play(self):
        self.plr.playCard(self.trans)
        self.assertEquals(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inReserve('Transmogrify'))

    def test_call(self):
        self.plr.setHand('Duchy', 'Estate')
        self.plr.setReserve('Transmogrify')
        self.plr.test_input = ['duchy', 'gold']
        self.plr.callReserve('Transmogrify')
        self.g.print_state()
        self.assertIsNotNone(self.g.inTrash('Duchy'))
        self.assertIsNotNone(self.plr.inHand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

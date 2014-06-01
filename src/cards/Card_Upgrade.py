#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Upgrade(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 card, +1 action. Trash a card and gain one costing 1 more"
        self.name = 'Upgrade'
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to 1 more than it """
        player.output("Trash a card from your hand. Gain a card costing exactly 1 more than it")
        tc = player.plrTrashCard(printcost=True)
        if tc:
            cost = player.cardCost(tc[0])
            player.plrGainCard(cost + 1, 'equal')


###############################################################################
class Test_Upgrade(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['upgrade'])
        self.plr = self.g.players[0]
        self.card = self.g['upgrade'].remove()

    def test_play(self):
        """ Play the Upgrade """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 6)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(self.g.trashpile, [])

    def test_trash(self):
        """ Trash an upgrade """
        self.plr.setHand('estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 2)
        self.assertEqual(self.plr.t['actions'], 1)
        self.assertEqual(len(self.g.trashpile), 1)
        self.assertEqual(self.g.trashpile[-1].name, 'Estate')
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertEqual(self.plr.discardpile[-1].cost, 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

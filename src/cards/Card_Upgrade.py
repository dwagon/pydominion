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
        tc = player.plrTrashCard(printcost=True, prompt="Trash a card from your hand. Gain a card costing exactly 1 more than it")
        if tc:
            cost = player.cardCost(tc[0])
            player.plrGainCard(cost + 1, 'equal')


###############################################################################
class Test_Upgrade(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Upgrade'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Upgrade'].remove()

    def test_play(self):
        """ Play the Upgrade """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertTrue(self.g.trashpile.isEmpty())

    def test_trash(self):
        """ Trash an upgrade """
        self.plr.setHand('Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.g.trashSize(), 1)
        self.assertEqual(self.g.trashpile[-1].name, 'Estate')
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.discardpile[-1].cost, 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Transmogrify(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.RESERVE]
        self.base = Game.ADVENTURE
        self.desc = """+1 Action; At the start of your turn, you may call this,
        to trash a card from your hand, gain a card costing up to 1 coin more
        than it, and put that card into your hand"""
        self.name = 'Transmogrify'
        self.actions = 1
        self.when = 'start'
        self.cost = 4

    def hook_call_reserve(self, game, player):
        tc = player.plrTrashCard(printcost=True, prompt="Trash a card from you hand. Gain a card costing up to 1 more")
        if tc:
            cost = player.cardCost(tc[0])
            player.plrGainCard(cost+1, modifier='less', destination='hand')


###############################################################################
class Test_Transmogrify(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Transmogrify'], badcards=['Duchess', "Fool's Gold"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.trans = self.g['Transmogrify'].remove()
        self.plr.addCard(self.trans, 'hand')

    def test_play(self):
        self.plr.playCard(self.trans)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.in_reserve('Transmogrify'))

    def test_call(self):
        self.plr.setHand('Duchy', 'Estate')
        self.plr.setReserve('Transmogrify')
        self.plr.test_input = ['trash duchy', 'get gold']
        self.plr.call_reserve('Transmogrify')
        self.assertIsNotNone(self.g.in_trash('Duchy'))
        self.assertIsNotNone(self.plr.in_hand('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

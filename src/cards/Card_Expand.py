#!/usr/bin/env python

import unittest
from Card import Card


class Card_Expand(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Trash a card from hand and gain one costing 3 more"
        self.name = 'Expand'
        self.cost = 7

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to
            3 more than the trashed card """
        player.output("Trash a card from your hand. Gain another costing up to 3 more than the one you trashed")
        tc = player.plrTrashCard(printcost=True)
        if tc:
            cost = tc[0].cost
            player.plrGainCard(cost + 3)


###############################################################################
class Test_Expand(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['expand'])
        self.plr = self.g.players[0]
        self.expand = self.g['expand'].remove()

    def test_play(self):
        self.plr.setHand('copper')
        self.plr.addCard(self.expand, 'hand')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.expand)
        self.assertEqual(self.plr.hand, [])
        self.assertEqual(len(self.plr.discardpile), 1)
        self.assertLessEqual(self.plr.discardpile[0].cost, 3)
        self.g.print_state()

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF

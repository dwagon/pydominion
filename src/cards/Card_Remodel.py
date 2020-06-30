#!/usr/bin/env python

import unittest
from Card import Card


class Card_Remodel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash a card and gain one costing 2 more"
        self.name = 'Remodel'
        self.cost = 2

    def special(self, game, player):
        """ Trash a card from your hand. Gain a card costing up to
            2 more than the trashed card """
        tc = player.plrTrashCard(printcost=True, prompt="Trash a card from your hand. Gain another costing up to 2 more than the one you trashed")
        if tc:
            cost = tc[0].cost
            player.plrGainCard(cost + 2)


###############################################################################
class Test_Remodel(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Remodel'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.rcard = self.g['Remodel'].remove()

    def test_nothing(self):
        tsize = self.g.trashSize()
        self.plr.addCard(self.rcard, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.rcard)
        self.assertEqual(self.g.trashSize(), tsize)
        self.assertEqual(self.plr.discardSize(), 0)
        self.assertEqual(self.plr.handSize(), 5)

    def test_trash_gainnothing(self):
        tsize = self.g.trashSize()
        self.plr.addCard(self.rcard, 'hand')
        self.plr.test_input = ['1', '0']
        self.plr.playCard(self.rcard)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertEqual(self.plr.discardSize(), 0)
        self.assertEqual(self.plr.handSize(), 4)

    def test_trash_gainsomething(self):
        tsize = self.g.trashSize()
        self.plr.addCard(self.rcard, 'hand')
        self.plr.test_input = ['1', '1']
        self.plr.playCard(self.rcard)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.handSize(), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

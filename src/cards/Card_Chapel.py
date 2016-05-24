#!/usr/bin/env python

import unittest
from Card import Card


class Card_Chapel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash up to 4 cards"
        self.name = 'Chapel'
        self.cost = 2

    def special(self, game, player):
        """ Trash up to 4 cards from your hand """
        player.output("Trash up to four cards")
        player.plrTrashCard(num=4)


###############################################################################
class Test_Chapel(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Chapel'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.ccard = self.g['Chapel'].remove()
        self.plr.setHand('Copper', 'Silver', 'Estate')
        self.plr.addCard(self.ccard, 'hand')

    def test_trashnone(self):
        self.plr.test_input = ['finish']
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.handSize(), 3)
        self.assertTrue(self.g.trashpile.isEmpty())

    def test_trashtwo(self):
        self.plr.test_input = ['trash copper', 'trash silver', 'finish']
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.handSize(), 1)
        self.assertEquals(self.g.trashSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

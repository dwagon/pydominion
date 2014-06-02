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
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['chapel'])
        self.plr = self.g.players[0]
        self.ccard = self.g['chapel'].remove()
        self.plr.setHand('estate', 'estate', 'estate')
        self.plr.addCard(self.ccard, 'hand')

    def test_trashnone(self):
        self.plr.test_input = ['0']
        self.plr.playCard(self.ccard)
        self.assertEquals(len(self.plr.hand), 3)
        self.assertEquals(self.g.trashpile, [])

    def test_trashtwo(self):
        self.plr.test_input = ['1', '2', '0']
        self.plr.playCard(self.ccard)
        self.assertEquals(len(self.plr.hand), 1)
        self.assertEquals(len(self.g.trashpile), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

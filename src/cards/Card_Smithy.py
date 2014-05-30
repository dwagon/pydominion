#!/usr/bin/env python

import unittest
from Card import Card


class Card_Smithy(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+3 cards"
        self.name = 'Smithy'
        self.cards = 3
        self.cost = 4


###############################################################################
class Test_Smithy(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['smithy'])
        self.plr = self.g.players[0]
        self.card = self.g['smithy'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the smithy """
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 8)


###############################################################################
if __name__ == "__main__":
    unittest.main()


#EOF

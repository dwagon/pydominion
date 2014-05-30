#!/usr/bin/env python

import unittest
from Card import Card


class Card_Moat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'dominion'
        self.desc = "+2 cards, defense"
        self.name = 'Moat'
        self.defense = True
        self.cost = 2
        self.cards = 2


###############################################################################
class Test_Library(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['moat'])
        self.plr = self.g.players[0]
        self.card = self.g['moat'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a moat """
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 7)

###############################################################################
if __name__ == "__main__":
    unittest.main()

#EOF

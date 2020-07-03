#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
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
class Test_Moat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a moat """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

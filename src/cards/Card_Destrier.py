#!/usr/bin/env python

import unittest
from Card import Card
import Game


###############################################################################
class Card_Destrier(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'menagerie'
        self.desc = "+2 Cards; +1 Action; During your turns, this costs 1 less per card you've gained this turn."
        self.name = 'Destrier'
        self.cards = 2
        self.actions = 1
        self.cost = 6

    def hook_thisCardCost(self, game, player):
        num_gained = len(player.stats['gained'])
        return -num_gained


###############################################################################
class Test_Destrier(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Destrier'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Destrier'].remove()

    def test_play(self):
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

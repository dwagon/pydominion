#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Laboratory(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DOMINION
        self.desc = "+2 cards, +1 action"
        self.name = 'Laboratory'
        self.cards = 2
        self.actions = 1
        self.cost = 5


###############################################################################
class Test_Laboratory(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Laboratory'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Laboratory'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Laboratory """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        # 5 hand, +2 for playing lab
        self.assertEqual(self.plr.handSize(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Festival(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DOMINION
        self.desc = "+2 actions, +1 buys, +2 coin"
        self.name = 'Festival'
        self.actions = 2
        self.buys = 1
        self.coin = 2
        self.cost = 5


###############################################################################
class Test_Festival(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Festival'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Festival'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

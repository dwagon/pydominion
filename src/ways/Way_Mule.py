#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Mule(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "+1 Action; +1 Coin"
        self.name = "Mule"
        self.actions = 1
        self.coin = 1


###############################################################################
class Test_Mule(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Mule'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()

    def test_play(self):
        """ Perform a Mule """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Mule']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

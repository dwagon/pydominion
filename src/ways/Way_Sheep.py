#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Sheep(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "+2 Coins"
        self.name = "Sheep"

    def special(self, game, player):
        player.addCoin(2)


###############################################################################
class Test_Sheep(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Sheep'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()

    def test_play(self):
        """ Perform a Sheep """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Sheep']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

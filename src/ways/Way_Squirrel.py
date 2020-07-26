#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Squirrel(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "+2 Cards at the end of this turn."
        self.name = "Squirrel"

    def special(self, game, player):
        player.newhandsize += 2


###############################################################################
class Test_Squirrel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Squirrel'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()

    def test_play(self):
        """ Perform a Squirrel """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Squirrel']
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.assertEqual(self.plr.handSize(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Otter(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "+2 Cards"
        self.name = "Way of the Otter"
        self.cards = 2


###############################################################################
class Test_Otter(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Way of the Otter'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Way of the Otter']

    def test_play(self):
        """ Perform a Otter """
        self.plr.addCard(self.card, 'hand')
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

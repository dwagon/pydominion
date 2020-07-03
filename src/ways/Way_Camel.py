#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Camel(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "Exile a Gold from the Supply."
        self.name = "Camel"

    def special(self, game, player):
        pass


###############################################################################
class Test_Camel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, eventcards=['Camel'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.ways['Camel']

    def test_play(self):
        """ Perform a Camel """
        self.plr.addCoin(10)
        self.plr.performWay(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Province'))
        self.assertIsNotNone(self.plr.inDiscard('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

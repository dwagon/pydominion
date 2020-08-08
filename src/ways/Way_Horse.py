#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Horse(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "+2 Cards; +1 Action; Return this to its pile."
        self.name = "Horse"
        self.cards = 2
        self.actions = 1

    def special_way(self, game, player, card):
        game[card.name].add()
        return {'discard': False}


###############################################################################
class Test_Horse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Horse'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Horse']

    def test_play(self):
        """ Perform a Horse """
        self.plr.addCard(self.card, 'hand')
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 2)
        self.assertEqual(self.g['Moat'].pilesize, 10)
        self.assertIsNone(self.plr.in_hand('Moat'))
        self.assertIsNone(self.plr.in_discard('Moat'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

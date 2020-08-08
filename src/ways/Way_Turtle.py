#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Turtle(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = 'menagerie'
        self.desc = "Set this aside. If you did, play it at the start of your next turn."
        self.name = "Turtle"
        self.actions = 2

    def special_way(self, game, player, card):
        player.defer_card(card)
        return {'discard': False}


###############################################################################
class Test_Turtle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Turtle'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Turtle']

    def test_play(self):
        """ Perform a Turtle """
        self.plr.addCard(self.card, 'hand')
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

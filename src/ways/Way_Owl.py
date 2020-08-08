#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Owl(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Draw until you have 6 cards in hand."
        self.name = "Owl"

    def special(self, game, player):
        player.pickUpHand(6)


###############################################################################
class Test_Owl(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Owl'], initcards=['Moat'], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Owl']

    def test_play(self):
        """ Perform a Owl """
        self.plr.setHand('Copper', 'Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.perform_way(self.way, self.card)
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

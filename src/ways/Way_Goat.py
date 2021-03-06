#!/usr/bin/env python

import unittest
import Game
from Way import Way


###############################################################################
class Way_Goat(Way):
    def __init__(self):
        Way.__init__(self)
        self.base = Game.MENAGERIE
        self.desc = "Trash a card from your hand."
        self.name = "Way of the Goat"

    def special(self, game, player):
        player.plrTrashCard()


###############################################################################
class Test_Goat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, waycards=['Way of the Goat'], initcards=['Moat'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()
        self.way = self.g.ways['Way of the Goat']

    def test_play(self):
        """ Perform a Goat """
        self.plr.setHand('Copper', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Copper']
        self.plr.perform_way(self.way, self.card)
        self.assertIsNotNone(self.g.in_trash('Copper'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

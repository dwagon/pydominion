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
        player.exile_card('Gold')


###############################################################################
class Test_Camel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, waycards=['Camel'],
            initcards=['Moat'], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Moat'].remove()

    def test_play(self):
        """ Perform a Camel """
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Camel']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.in_exile('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

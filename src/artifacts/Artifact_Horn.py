#!/usr/bin/env python

import unittest
import Game
from Artifact import Artifact


###############################################################################
class Artifact_Horn(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.base = Game.RENAISSANCE
        self.desc = "Once per turn, when you discard a Border Guard from play, you may put it onto your deck."
        self.name = "Horn"


###############################################################################
class Test_Horn(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=['Horn'], initcards=['Border Guard'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.artifact = self.g.artifacts['Horn']
        self.card = self.g['Border Guard'].remove()

    def test_horn(self):
        self.plr.assign_artifact('Horn')
        self.plr.test_input = ['Put into hand']
        self.plr.discardCard(self.card)
        self.assertIsNotNone(self.plr.in_deck('Border Guard'))
        self.assertIsNone(self.plr.in_discard('Border Guard'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

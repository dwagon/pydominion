#!/usr/bin/env python

import unittest
from Artifact import Artifact


###############################################################################
class Artifact_Lantern(Artifact):
    def __init__(self):
        Artifact.__init__(self)
        self.cardtype = 'artifact'
        self.base = 'renaissance'
        self.desc = "Your Border Guards reveal 3 cards and discard 2. (It takes all 3 being Actions to take the Horn.)"
        self.name = "Lantern"


###############################################################################
class Test_Lantern(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initartifacts=['Lantern'], initcards=['Border Guard', 'Moat', 'Guide'])
        self.g.start_game()
        self.plr = self.g.playerList(0)
        self.artifact = self.g.artifacts['Lantern']
        self.card = self.g['Border Guard'].remove()
        self.plr.assign_artifact('Lantern')

    def test_play(self):
        self.plr.setDeck('Province', 'Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Select Gold']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getActions(), 1)
        self.assertIsNotNone(self.plr.inHand('Gold'))
        self.assertIsNotNone(self.plr.inDiscard('Silver'))
        self.assertIsNotNone(self.plr.inDiscard('Province'))

    def test_play_actions(self):
        self.plr.setDeck('Guide', 'Moat', 'Guide')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Select Moat', 'Take Horn']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inHand('Moat'))
        self.assertIsNotNone(self.plr.inDiscard('Guide'))
        self.assertTrue(self.plr.has_artifact('Horn'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

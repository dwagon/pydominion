#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_load_travellers(unittest.TestCase):
    def test_needtravellers(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['page'])
        self.g.startGame()
        self.assertTrue(self.g.needtravellers)


###############################################################################
class Test_replace_traveller(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['page'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['page'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_replace(self):
        """ Replace a traveller """
        self.plr.test_input = ['replace']
        self.plr.playCard(self.card)
        self.plr.replace_traveller(self.card, 'TreasureHunter')
        self.assertIsNone(self.plr.inHand('Page'))
        self.assertIsNotNone(self.plr.inHand('TreasureHunter'))

    def test_dont_replace(self):
        """ Choose not to replace a traveller """
        self.plr.test_input = ['keep']
        self.plr.replace_traveller(self.card, 'TreasureHunter')
        self.assertIsNotNone(self.plr.inHand('Page'))
        self.assertIsNone(self.plr.inHand('TreasureHunter'))

    def test_replacement_not_available(self):
        """ Try and replace a traveller when the replacement isn't available """
        self.plr.test_input = ['replace']
        # TODO

    def test_not_played(self):
        """ Try and replace a traveller when it hasn't been played """
        self.plr.test_input = ['replace']
        self.plr.replace_traveller(self.card, 'TreasureHunter')
        self.assertIsNotNone(self.plr.inHand('Page'))
        self.assertIsNone(self.plr.inHand('TreasureHunter'))

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

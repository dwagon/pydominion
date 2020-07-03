#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_is_card(unittest.TestCase):
    def test_isDuration(self):
        """ Test isDuration """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Caravan', 'Moat'])
        g.start_game()
        caravan = g['Caravan'].remove()
        moat = g['Moat'].remove()
        self.assertTrue(caravan.isDuration())
        self.assertFalse(moat.isDuration())

    def test_isTreasure(self):
        """ Test isTreasure """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Counterfeit', 'Moat'])
        g.start_game()
        counterfeit = g['Counterfeit'].remove()
        moat = g['Moat'].remove()
        self.assertTrue(counterfeit.isTreasure())
        self.assertFalse(moat.isTreasure())

    def test_isLooter(self):
        """ Test isLooter """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Cultist', 'Moat'])
        g.start_game()
        cultist = g['Cultist'].remove()
        moat = g['Moat'].remove()
        self.assertTrue(cultist.isLooter())
        self.assertFalse(moat.isLooter())

    def test_isAction(self):
        """ Test isAction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Cultist', 'Vineyard'])
        g.start_game()
        cultist = g['Cultist'].remove()
        vineyard = g['Vineyard'].remove()
        self.assertTrue(cultist.isAction())
        self.assertFalse(vineyard.isAction())

    def test_isTraveller(self):
        """ Test isTraveller """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Page', 'Vineyard'])
        g.start_game()
        page = g['Page'].remove()
        vineyard = g['Vineyard'].remove()
        self.assertTrue(page.isTraveller())
        self.assertFalse(vineyard.isTraveller())

    def test_isReaction(self):
        """ Test isReaction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Page', 'Moat'])
        g.start_game()
        page = g['Page'].remove()
        moat = g['Moat'].remove()
        self.assertTrue(moat.isReaction())
        self.assertFalse(page.isReaction())

    def test_isNight(self):
        """ Test isReaction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Monastery', 'Moat'])
        g.start_game()
        monastery = g['Monastery'].remove()
        moat = g['Moat'].remove()
        self.assertTrue(monastery.isNight())
        self.assertFalse(moat.isNight())

    def test_isAttack(self):
        """ Test isReaction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['Militia', 'Moat'])
        g.start_game()
        militia = g['Militia'].remove()
        moat = g['Moat'].remove()
        self.assertTrue(militia.isAttack())
        self.assertFalse(moat.isAttack())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

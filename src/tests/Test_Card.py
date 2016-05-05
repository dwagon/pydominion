#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_is_card(unittest.TestCase):
    def test_isDuration(self):
        """ Test isDuration """
        g = Game.Game(quiet=True, numplayers=1, initcards=['caravan', 'moat'])
        g.startGame()
        caravan = g['caravan'].remove()
        moat = g['moat'].remove()
        self.assertTrue(caravan.isDuration())
        self.assertFalse(moat.isDuration())

    def test_isTreasure(self):
        """ Test isTreasure """
        g = Game.Game(quiet=True, numplayers=1, initcards=['counterfeit', 'moat'])
        g.startGame()
        counterfeit = g['counterfeit'].remove()
        moat = g['moat'].remove()
        self.assertTrue(counterfeit.isTreasure())
        self.assertFalse(moat.isTreasure())

    def test_isLooter(self):
        """ Test isLooter """
        g = Game.Game(quiet=True, numplayers=1, initcards=['cultist', 'moat'])
        g.startGame()
        cultist = g['cultist'].remove()
        moat = g['moat'].remove()
        self.assertTrue(cultist.isLooter())
        self.assertFalse(moat.isLooter())

    def test_isAction(self):
        """ Test isAction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['cultist', 'vineyard'])
        g.startGame()
        cultist = g['cultist'].remove()
        vineyard = g['vineyard'].remove()
        self.assertTrue(cultist.isAction())
        self.assertFalse(vineyard.isAction())

    def test_isTraveller(self):
        """ Test isTraveller """
        g = Game.Game(quiet=True, numplayers=1, initcards=['page', 'vineyard'])
        g.startGame()
        page = g['page'].remove()
        vineyard = g['vineyard'].remove()
        self.assertTrue(page.isTraveller())
        self.assertFalse(vineyard.isTraveller())

    def test_isReaction(self):
        """ Test isReaction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['page', 'moat'])
        g.startGame()
        page = g['page'].remove()
        moat = g['moat'].remove()
        self.assertTrue(moat.isReaction())
        self.assertFalse(page.isReaction())

    def test_isAttack(self):
        """ Test isReaction """
        g = Game.Game(quiet=True, numplayers=1, initcards=['militia', 'moat'])
        g.startGame()
        militia = g['militia'].remove()
        moat = g['moat'].remove()
        self.assertTrue(militia.isAttack())
        self.assertFalse(moat.isAttack())

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

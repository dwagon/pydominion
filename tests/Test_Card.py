#!/usr/bin/env python

import unittest

from dominion import Game


###############################################################################
class Test_is_card(unittest.TestCase):
    def test_isDuration(self):
        """Test isDuration"""
        g = Game.TestGame(numplayers=1, initcards=["Caravan", "Moat"])
        g.start_game()
        caravan = g.get_card_from_pile("Caravan")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(caravan.isDuration())
        self.assertFalse(moat.isDuration())

    def test_isTreasure(self):
        """Test isTreasure"""
        g = Game.TestGame(numplayers=1, initcards=["Counterfeit", "Moat"])
        g.start_game()
        counterfeit = g.get_card_from_pile("Counterfeit")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(counterfeit.isTreasure())
        self.assertFalse(moat.isTreasure())

    def test_isLooter(self):
        """Test isLooter"""
        g = Game.TestGame(numplayers=1, initcards=["Cultist", "Moat"])
        g.start_game()
        cultist = g.get_card_from_pile("Cultist")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(cultist.isLooter())
        self.assertFalse(moat.isLooter())

    def test_isAction(self):
        """Test isAction"""
        g = Game.TestGame(numplayers=1, initcards=["Cultist", "Vineyard"])
        g.start_game()
        cultist = g.get_card_from_pile("Cultist")
        vineyard = g.get_card_from_pile("Vineyard")
        self.assertTrue(cultist.isAction())
        self.assertFalse(vineyard.isAction())

    def test_isTraveller(self):
        """Test isTraveller"""
        g = Game.TestGame(numplayers=1, initcards=["Page", "Vineyard"])
        g.start_game()
        page = g.get_card_from_pile("Page")
        vineyard = g.get_card_from_pile("Vineyard")
        self.assertTrue(page.isTraveller())
        self.assertFalse(vineyard.isTraveller())

    def test_isReaction(self):
        """Test isReaction"""
        g = Game.TestGame(numplayers=1, initcards=["Page", "Moat"])
        g.start_game()
        page = g.get_card_from_pile("Page")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(moat.isReaction())
        self.assertFalse(page.isReaction())

    def test_isNight(self):
        """Test isReaction"""
        g = Game.TestGame(numplayers=1, initcards=["Monastery", "Moat"])
        g.start_game()
        monastery = g.get_card_from_pile("Monastery")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(monastery.isNight())
        self.assertFalse(moat.isNight())

    def test_isAttack(self):
        """Test isReaction"""
        g = Game.TestGame(numplayers=1, initcards=["Militia", "Moat"])
        g.start_game()
        militia = g.get_card_from_pile("Militia")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(militia.isAttack())
        self.assertFalse(moat.isAttack())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""Tests for Card class"""
import unittest

from dominion import Game, Piles


###############################################################################
class TestCard(unittest.TestCase):
    """Test Card functions"""

    def test_description(self):
        """Test description changing"""
        g = Game.TestGame(numplayers=1, initcards=["Description"], card_path="tests/cards")
        g.start_game()
        plr = g.player_list()[0]
        g.start_game()
        card = g.get_card_from_pile("Description")
        plr.add_card(card, Piles.HAND)
        self.assertEqual(card.description(plr), "Foo Bar")


###############################################################################
class TestIsCard(unittest.TestCase):
    """Test is_types() of cards"""

    def test_isDuration(self) -> None:
        """Test isDuration"""
        g = Game.TestGame(numplayers=1, initcards=["Caravan", "Moat"])
        g.start_game()
        caravan = g.get_card_from_pile("Caravan")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(caravan.isDuration())
        self.assertFalse(moat.isDuration())

    def test_dynamic_card_type(self) -> None:
        """Test dynamic card type"""
        g = Game.TestGame(numplayers=1, initcards=["Dyna Type"], card_path="tests/cards")
        g.start_game()
        plr = g.player_list()[0]
        copper = g.get_card_from_pile("Copper")
        dyna = g.get_card_from_pile("Dyna Type")
        plr.add_card(copper, Piles.HAND)
        self.assertFalse(copper.isNight())
        plr.add_card(dyna, Piles.HAND)
        self.assertTrue(copper.isNight())

    def test_isTreasure(self) -> None:
        """Test isTreasure"""
        g = Game.TestGame(numplayers=1, initcards=["Counterfeit", "Moat"])
        g.start_game()
        counterfeit = g.get_card_from_pile("Counterfeit")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(counterfeit.isTreasure())
        self.assertFalse(moat.isTreasure())

    def test_isLooter(self) -> None:
        """Test isLooter"""
        g = Game.TestGame(numplayers=1, initcards=["Cultist", "Moat"])
        g.start_game()
        cultist = g.get_card_from_pile("Cultist")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(cultist.isLooter())
        self.assertFalse(moat.isLooter())

    def test_isAction(self) -> None:
        """Test isAction"""
        g = Game.TestGame(numplayers=1, initcards=["Cultist", "Vineyard"])
        g.start_game()
        cultist = g.get_card_from_pile("Cultist")
        vineyard = g.get_card_from_pile("Vineyard")
        self.assertTrue(cultist.isAction())
        self.assertFalse(vineyard.isAction())

    def test_isTraveller(self) -> None:
        """Test isTraveller"""
        g = Game.TestGame(numplayers=1, initcards=["Page", "Vineyard"])
        g.start_game()
        page = g.get_card_from_pile("Page")
        vineyard = g.get_card_from_pile("Vineyard")
        self.assertTrue(page.isTraveller())
        self.assertFalse(vineyard.isTraveller())

    def test_isReaction(self) -> None:
        """Test isReaction"""
        g = Game.TestGame(numplayers=1, initcards=["Page", "Moat"])
        g.start_game()
        page = g.get_card_from_pile("Page")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(moat.isReaction())
        self.assertFalse(page.isReaction())

    def test_isNight(self) -> None:
        """Test isReaction"""
        g = Game.TestGame(numplayers=1, initcards=["Monastery", "Moat"])
        g.start_game()
        monastery = g.get_card_from_pile("Monastery")
        moat = g.get_card_from_pile("Moat")
        self.assertTrue(monastery.isNight())
        self.assertFalse(moat.isNight())

    def test_isAttack(self) -> None:
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

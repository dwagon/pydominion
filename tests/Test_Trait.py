#!/usr/bin/env python
"""Test Traits"""
import unittest

from dominion import Game


###############################################################################
class Test_Traits(unittest.TestCase):
    """Testing on traits"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["TestTrait", "Moat"], trait_path="tests/traits")
        self.g.start_game()

    def test_isTraitCard(self) -> None:
        """Test isTraitCard"""
        trait = self.g.traits["TestTrait"]
        moat = self.g.get_card_from_pile("Moat")
        self.assertFalse(trait.isTraitCard(self.g, moat))
        self.g.assign_trait("TestTrait", "Moat")
        self.assertTrue(trait.isTraitCard(self.g, moat))

    def test_description(self) -> None:
        """Test trait gets added to card description"""
        self.g.assign_trait("TestTrait", "Moat")
        moat = self.g.get_card_from_pile("Moat")
        self.assertIn("TestTrait", moat.description(self.g.player_list()[0]))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
""" Test the Game module """
# pylint: disable=invalid-name, protected-access, fixme

import unittest
from dominion import Game


###############################################################################
class TestArgs(unittest.TestCase):
    """Test argument parsing"""

    def setUp(self):
        pass

    def test_numplayers(self):
        """TODO"""
        g = Game.TestGame(numplayers=4)
        g.start_game()
        self.assertEqual(len(g.player_list()), 4)

    def test_card(self):
        """TODO"""
        g = Game.TestGame(initcards=["Moat"])
        g.start_game()
        self.assertIn("Moat", g.card_piles)

    def test_basecard(self):
        """Make sure that if you specify a basecard in initcards it works"""
        g = Game.TestGame(initcards=["Platinum"])
        g.start_game()
        self.assertIn("Platinum", g.card_piles)

    def test_prosperity(self):
        """TODO"""
        g = Game.TestGame(prosperity=True)
        g.start_game()
        self.assertIn("Colony", g.card_piles)
        self.assertIn("Platinum", g.card_piles)

    def test_event(self):
        """Test that we can specify an event on the command line"""
        g = Game.TestGame(events=["Alms"])
        g.start_game()
        self.assertIn("Alms", g.events)

    def test_old_cards(self):
        """Can we access old cards"""
        g = Game.TestGame(card_path="tests/cards", oldcards=True)
        g.start_game()
        self.assertIn("OldCard", g.card_piles)

    def test_potions(self):
        """Test Specifying potions"""
        g = Game.TestGame(card_path="tests/cards", potions=True, cards=["Pot Cost"])
        g.start_game()
        self.assertIn("Pot Cost", g.card_piles)
        g = Game.TestGame(card_path="tests/cards", potions=False, cards=["Pot Cost"])
        g.start_game()
        self.assertNotIn("Pot Cost", g.card_piles)


###############################################################################
class TestGuessCardname(unittest.TestCase):
    """TODO"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2)
        self.g.start_game()

    def test_guesses(self):
        """TODO"""
        self.assertEqual(self.g.guess_card_name("moat"), "Moat")
        self.assertEqual(self.g.guess_card_name("grandmarket"), "Grand Market")
        self.assertEqual(
            self.g.guess_card_name("philosophersstone"), "Philosopher's Stone"
        )
        self.assertEqual(self.g.guess_card_name("colony", prefix="BaseCard"), "Colony")
        self.assertIsNone(self.g.guess_card_name("nosuchcard"))


###############################################################################
class TestGameOver(unittest.TestCase):
    """Test detecting when the game is over"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=2)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_not_over(self):
        """The game isn't over yet"""
        over = self.g.isGameOver()
        self.assertFalse(over)

    def test_provinces(self):
        """Someone took the last province"""
        while self.g.card_piles["Province"]:
            card = self.plr.gain_card("Province")
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_three_stacks(self):
        """Three stacks are empty"""
        while self.g.card_piles["Estate"]:
            self.plr.gain_card("Estate")
        while self.g.card_piles["Copper"]:
            self.plr.gain_card("Copper")
        while self.g.card_piles["Silver"]:
            self.plr.gain_card("Silver")
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_two_stacks(self):
        """Two stacks are empty"""
        while self.g.card_piles["Estate"]:
            self.plr.gain_card("Estate")
        while self.g.card_piles["Silver"]:
            self.plr.gain_card("Silver")
        over = self.g.isGameOver()
        self.assertFalse(over)


###############################################################################
class TestActionPiles(unittest.TestCase):
    """Test get_action_piles()"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.g.start_game()

    def test_action_piles(self):
        piles = self.g.get_action_piles()
        self.assertIn("Moat", piles)
        self.assertNotIn("Copper", piles)


###############################################################################
class TestTreasurePiles(unittest.TestCase):
    """Test get_treasure_piles()"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.g.start_game()

    def test_treasure_piles(self):
        piles = self.g.get_treasure_piles()
        self.assertNotIn("Moat", piles)
        self.assertIn("Copper", piles)


###############################################################################
class Test_boon(unittest.TestCase):
    # TODO - convert to using real boons rather than letters
    def setUp(self):
        self.g = Game.TestGame(numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_receive_boon_empty(self):
        self.g.boons = []
        self.g.discarded_boons = ["a", "b", "c", "d"]
        b = self.g.receive_boon()
        self.assertIn(b, ["a", "b", "c", "d"])
        self.assertEqual(self.g.discarded_boons, [])
        self.assertEqual(len(self.g.boons), 3)
        self.assertNotIn(b, self.g.boons)

    def test_receive_boon_non_empty(self):
        self.g.boons = ["a", "b"]
        self.g.discarded_boons = ["c", "d"]
        b = self.g.receive_boon()
        self.assertIn(b, ["a", "b"])
        self.assertEqual(self.g.discarded_boons, ["c", "d"])
        self.assertEqual(len(self.g.boons), 1)
        self.assertNotIn(b, self.g.boons)


###############################################################################
class TestWhoWon(unittest.TestCase):
    def setUp(self):
        self.numplayers = 3
        self.g = Game.TestGame(numplayers=self.numplayers, badcards=["Shepherd"])
        self.g.start_game()

    def test_whoWon(self):
        scores = self.g.whoWon()
        # Everyone should get 3 estates at start
        for score in scores.values():
            self.assertEqual(score, 3)
        self.assertEqual(len(scores), self.numplayers)


###############################################################################
class TestAssignTrait(unittest.TestCase):
    """Test assign_trait()"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, traits=["Cheap"], initcards=["Moat"])
        self.g.start_game()

    def test_assign(self):
        self.g.assign_trait("Cheap", "Moat")
        self.assertEqual(self.g.card_piles["Moat"].trait, "Cheap")
        self.assertEqual(self.g.traits["Cheap"].card_pile, "Moat")


###############################################################################
class TestGetCardFromPile(unittest.TestCase):
    """Test get_card_from_pile()"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1)
        self.g.start_game()

    def test_get_card(self):
        pile_size = len(self.g.card_piles["Copper"])
        card = self.g.get_card_from_pile("Copper")
        self.assertEqual(card.name, "Copper")
        self.assertEqual(len(self.g.card_piles["Copper"]), pile_size - 1)

    def test_get_wrong_card(self):
        """Test asking for a wrong card"""
        pile_size = len(self.g.card_piles["Copper"])
        self.assertIsNone(self.g.get_card_from_pile("Copper", "Gold"))
        self.assertEqual(len(self.g.card_piles["Copper"]), pile_size)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

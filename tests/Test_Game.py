#!/usr/bin/env python
"""Test the Game module"""
# pylint: disable=invalid-name, protected-access, fixme

import unittest

from dominion import Game, NoCardException
from dominion.game_setup import guess_card_name


###############################################################################
class TestArgs(unittest.TestCase):
    """Test argument parsing"""

    def setUp(self) -> None:
        pass

    def test_numplayers(self) -> None:
        """TODO"""
        g = Game.TestGame(numplayers=4)
        g.start_game()
        self.assertEqual(len(g.player_list()), 4)

    def test_card(self) -> None:
        """TODO"""
        g = Game.TestGame(initcards=["Moat"])
        g.start_game()
        self.assertIn("Moat", g.card_piles)

    def test_basecard(self) -> None:
        """Make sure that if you specify a basecard in initcards it works"""
        g = Game.TestGame(initcards=["Platinum"])
        g.start_game()
        self.assertIn("Platinum", g.card_piles)

    def test_prosperity(self) -> None:
        """TODO"""
        g = Game.TestGame(prosperity=True)
        g.start_game()
        self.assertIn("Colony", g.card_piles)
        self.assertIn("Platinum", g.card_piles)

    def test_event(self) -> None:
        """Test that we can specify an event on the command line"""
        g = Game.TestGame(events=["Alms"])
        g.start_game()
        self.assertIn("Alms", g.events)

    def test_old_cards(self) -> None:
        """Can we access old cards"""
        g = Game.TestGame(card_path="tests/cards", oldcards=True)
        g.start_game()
        self.assertIn("OldCard", g.card_piles)

    def test_potions(self) -> None:
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

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2)
        self.g.start_game()

    def test_guesses(self) -> None:
        """TODO"""
        self.assertEqual(guess_card_name(self.g, "moat"), "Moat")
        self.assertEqual(guess_card_name(self.g, "grandmarket"), "Grand Market")
        self.assertEqual(guess_card_name(self.g, "philosophersstone"), "Philosopher's Stone")
        self.assertEqual(guess_card_name(self.g, "colony", prefix="BaseCard"), "Colony")
        self.assertIsNone(guess_card_name(self.g, "nosuchcard"))


###############################################################################
class TestGameOver(unittest.TestCase):
    """Test detecting when the game is over"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_not_over(self) -> None:
        """The game isn't over yet"""
        over = self.g.isGameOver()
        self.assertFalse(over)

    def test_provinces(self) -> None:
        """Someone took the last province"""
        while self.g.card_piles["Province"]:
            card = self.plr.gain_card("Province")
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_three_stacks(self) -> None:
        """Three stacks are empty"""
        while self.g.card_piles["Estate"]:
            self.plr.gain_card("Estate")
        while self.g.card_piles["Copper"]:
            self.plr.gain_card("Copper")
        while self.g.card_piles["Silver"]:
            self.plr.gain_card("Silver")
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_two_stacks(self) -> None:
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

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.g.start_game()

    def test_action_piles(self) -> None:
        piles = self.g.get_action_piles()
        self.assertIn("Moat", piles)
        self.assertNotIn("Copper", piles)


###############################################################################
class TestTreasurePiles(unittest.TestCase):
    """Test get_treasure_piles()"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, initcards=["Moat"])
        self.g.start_game()

    def test_treasure_piles(self) -> None:
        piles = self.g.get_treasure_piles()
        self.assertNotIn("Moat", piles)
        self.assertIn("Copper", piles)


###############################################################################
class Test_boon(unittest.TestCase):
    # TODO - convert to using real boons rather than letters
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_receive_boon_empty(self) -> None:
        self.g.boons = []
        self.g.discarded_boons = ["a", "b", "c", "d"]
        b = self.g.receive_boon()
        self.assertIn(b, ["a", "b", "c", "d"])
        self.assertEqual(self.g.discarded_boons, [])
        self.assertEqual(len(self.g.boons), 3)
        self.assertNotIn(b, self.g.boons)

    def test_receive_boon_non_empty(self) -> None:
        self.g.boons = ["a", "b"]
        self.g.discarded_boons = ["c", "d"]
        b = self.g.receive_boon()
        self.assertIn(b, ["a", "b"])
        self.assertEqual(self.g.discarded_boons, ["c", "d"])
        self.assertEqual(len(self.g.boons), 1)
        self.assertNotIn(b, self.g.boons)


###############################################################################
class TestWhoWon(unittest.TestCase):
    def setUp(self) -> None:
        self.numplayers = 3
        self.g = Game.TestGame(numplayers=self.numplayers, badcards=["Shepherd"])
        self.g.start_game()

    def test_whoWon(self) -> None:
        scores = self.g.whoWon()
        # Everyone should get 3 estates at start
        for score in scores.values():
            self.assertEqual(score, 3)
        self.assertEqual(len(scores), self.numplayers)


###############################################################################
class TestProphecies(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=2, initcards=["Mountain Shrine"], badcards=["Kind Emperor"])
        self.g.start_game()

    def test_sun_counters(self) -> None:
        self.assertIsNotNone(self.g.inactive_prophecy)
        self.assertIsNone(self.g.prophecy)
        self.assertEqual(self.g.sun_tokens, 5)
        self.g.remove_sun_token()
        self.assertEqual(self.g.sun_tokens, 4)

    def test_reveal_prophecy(self) -> None:
        self.assertIsNotNone(self.g.inactive_prophecy)
        self.assertIsNone(self.g.prophecy)
        for i in range(6):
            self.g.remove_sun_token()
        self.assertIsNotNone(self.g.prophecy)


###############################################################################
class TestAssignTrait(unittest.TestCase):
    """Test assign_trait()"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1, traits=["Cheap"], initcards=["Moat"])
        self.g.start_game()

    def test_assign(self) -> None:
        self.g.assign_trait("Cheap", "Moat")
        self.assertEqual(self.g.card_piles["Moat"].trait, "Cheap")
        self.assertEqual(self.g.traits["Cheap"].card_pile, "Moat")


###############################################################################
class TestGetCardFromPile(unittest.TestCase):
    """Test get_card_from_pile()"""

    def setUp(self) -> None:
        self.g = Game.TestGame(numplayers=1)
        self.g.start_game()

    def test_get_card(self) -> None:
        pile_size = len(self.g.card_piles["Copper"])
        card = self.g.get_card_from_pile("Copper")
        self.assertEqual(card.name, "Copper")
        self.assertEqual(len(self.g.card_piles["Copper"]), pile_size - 1)

    def test_get_wrong_card(self) -> None:
        """Test asking for a wrong card"""
        pile_size = len(self.g.card_piles["Copper"])
        with self.assertRaises(NoCardException):
            self.g.get_card_from_pile("Copper", "Gold")
        self.assertEqual(len(self.g.card_piles["Copper"]), pile_size)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

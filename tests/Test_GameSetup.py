#!/usr/bin/env python
"""Test the game_setup code"""

import unittest

from dominion import Game, game_setup, Card


###############################################################################
class TestUseSheltersInGame(unittest.TestCase):
    """Test use_shelters_in_game()"""

    def setUp(self):
        self.g = Game.Game()

    def test_allow_shelters(self):
        """If we forbid allow_shelters it should return False"""
        self.assertFalse(game_setup.use_shelters_in_game(self.g, False, []))

    def test_specify_shelters(self):
        """If we specify shelters then we are using shelters"""
        self.assertTrue(game_setup.use_shelters_in_game(self.g, True, ["shelters"]))

    def test_no_darkages(self):
        """If none of the cards are dark ages we shouldn't use shelters."""
        self.g = Game.TestGame()
        game_setup.load_decks(
            self.g,
            initcards=[
                "Cellar",
                "Chapel",
                "Moat",
                "Harbinger",
                "Merchant",
                "Vassal",
                "Village",
                "Workshop",
                "Gardens",
                "Militia",
            ],
            numstacks=10,
        )
        self.assertFalse(game_setup.use_shelters_in_game(self.g, True, []))

    def test_darkages(self):
        """If the cards are dark ages we should use shelters"""
        self.g = Game.TestGame()
        # The only way we can ensure a random choice is a dar kages is to make all the cards dark ages.
        game_setup.load_decks(
            self.g,
            initcards=[
                "Poor House",
                "Beggar",
                "Squire",
                "Vagrant",
                "Forager",
                "Hermit",
                "Sage",
                "Storeroom",
                "Urchin",
                "Mystic",
            ],
            numstacks=10,
        )
        self.assertTrue(game_setup.use_shelters_in_game(self.g, True, []))


###############################################################################
class TestSetupShelters(unittest.TestCase):
    """Test setup_shelters()"""

    def test_shelters(self):
        """Ensure setup shelters creates shelters"""
        g = Game.TestGame()
        game_setup.setup_shelters(g)
        self.assertIn("Shelters", g.card_piles)
        self.assertIn("Hovel", g.card_instances)


###############################################################################
class TestLoadLoot(unittest.TestCase):
    """Test load_loot()"""

    def test_loot(self):
        """Ensure loots are loaded"""
        g = Game.TestGame()
        game_setup.load_loot(g)
        self.assertIn("Loot", g.card_piles)


###############################################################################
class TestLoadWays(unittest.TestCase):
    """Test load_ways()"""

    def test_short_name_ways(self):
        """Ensure ways are loaded without full name"""
        g = Game.TestGame(way_path="tests/ways")
        ways = game_setup.load_ways(g, ["Test"], 1)
        self.assertEqual(list(ways.keys()), ["Way of the Test"])

    def test_full_name_ways(self):
        """Ensure ways are loaded without full name"""
        g = Game.TestGame(way_path="tests/ways")
        ways = game_setup.load_ways(g, ["Way of the Test"], 1)
        self.assertEqual(list(ways.keys()), ["Way of the Test"])
        self.assertEqual(ways["Way of the Test"].base, Card.CardExpansion.TEST)


###############################################################################
class TestLoadEvents(unittest.TestCase):
    """Test load_events()"""

    def test_load_events(self):
        """Ensure specified events are loaded"""
        g = Game.TestGame(event_path="tests/events")
        events = game_setup.load_events(g, ["Test"], 1)
        self.assertEqual(list(events.keys()), ["Test"])
        self.assertEqual(events["Test"].cost, 0)


###############################################################################
class TestLoadHexes(unittest.TestCase):
    """Test load_hexes()"""

    def test_load_hexes(self):
        """Ensure all hexes are loaded"""
        g = Game.TestGame(hex_path="tests/hexes")
        hexes = game_setup.load_hexes(g)
        self.assertEqual(len(hexes), 1)
        self.assertEqual(hexes[0].name, "Test Hex")


###############################################################################
class TestLoadProjects(unittest.TestCase):
    """Test load_projects()"""

    def test_load_projects(self):
        """Ensure specified projects are loaded"""
        g = Game.TestGame(project_path="tests/projects")
        projects = game_setup.load_projects(g, ["ProjectA"], 1)
        self.assertEqual(list(projects.keys()), ["ProjectA"])
        self.assertEqual(projects["ProjectA"].cost, 3)


###############################################################################
class TestLoadProphecies(unittest.TestCase):
    """Test load_prophecies()"""

    def test_load_prophecies(self):
        """Ensure specified prophecies are loaded"""
        g = Game.TestGame(prophecies_path="tests/prophecies")
        prophecy = game_setup.load_prophecies(g, ["Test"])
        self.assertEqual(prophecy.name, "Test")
        self.assertEqual(prophecy.base, Card.CardExpansion.TEST)


###############################################################################
class TestLoadArtifacts(unittest.TestCase):
    """Test load_artifacts()"""

    def test_load_artifacts(self):
        """Ensure all artifacts are loaded"""
        g = Game.TestGame(artifact_path="tests/artifacts")
        artifacts = game_setup.load_artifacts(g)
        self.assertEqual(len(artifacts), 1)
        self.assertEqual(artifacts["Test"].name, "Test")
        self.assertEqual(artifacts["Test"].base, Card.CardExpansion.TEST)


###############################################################################
class TestLoadLandmarks(unittest.TestCase):
    """Test load_landmarks()"""

    def test_load_landmarks(self):
        """Ensure landmarks are loaded"""
        g = Game.TestGame(landmark_path="tests/landmarks")
        landmarks = game_setup.load_landmarks(g, ["Test"], 1)
        self.assertEqual(len(landmarks), 1)
        self.assertEqual(landmarks["Test"].name, "Test")
        self.assertEqual(landmarks["Test"].base, Card.CardExpansion.TEST)


###############################################################################
class TestCardPileForTrait(unittest.TestCase):
    """Test card_pile_for_trait()"""

    def setUp(self):
        self.g = Game.TestGame(trait_path="tests/traits", initcards=["Moat"])
        self.g.start_game()

    def test_card_pile_for_trait(self):
        """Ensure card_piles for traits work"""
        # Not sure how to make this test actually be useful
        pile = game_setup.card_pile_for_trait(self.g)
        self.assertTrue(self.g.card_instances[pile].isAction() or self.g.card_instances[pile].isTreasure())
        self.assertTrue(self.g.card_instances[pile].purchasable)


###############################################################################
class TestCardPilesForTrait(unittest.TestCase):
    """Test card_piles_for_trait()"""

    def setUp(self):
        self.g = Game.TestGame(trait_path="tests/traits", initcards=["Moat", "Militia", "Teacher"])
        self.g.start_game()

    def test_with_traits(self):
        """Ensure piles with traits aren't listed"""
        game_setup.load_traits(self.g, ["TestTrait"], 1)
        self.g.assign_trait("TestTrait", "Militia")
        self.assertIn("Moat", game_setup.card_piles_for_trait(self.g))
        self.g.assign_trait("TestTrait", "Moat")
        self.assertNotIn("Moat", game_setup.card_piles_for_trait(self.g))

    def test_base_cards(self):
        """Ensure base cards aren't in the list"""
        self.assertNotIn("Silver", game_setup.card_piles_for_trait(self.g))

    def test_purchasable(self):
        """Ensure not purchasable cards aren't in the list"""
        self.assertNotIn("Teacher", game_setup.card_piles_for_trait(self.g))


###############################################################################
class TestLoadTraits(unittest.TestCase):
    """Test load_traits()"""

    def test_load_traits(self):
        """Ensure traits are loaded"""

        def test_select(_: Game) -> str:
            return "Moat"

        g = Game.TestGame(trait_path="tests/traits", initcards=["Moat"])
        g.start_game()  # Need to instantiate card piles first
        game_setup.load_traits(g, ["TestTrait"], 1, test_select)
        self.assertEqual(list(g.traits.keys()), ["TestTrait"])
        self.assertEqual(g.card_piles["Moat"].trait, "TestTrait")
        self.assertEqual(g.traits["TestTrait"].card_pile, "Moat")


###############################################################################
class TestLoadStates(unittest.TestCase):
    """Test load_states()"""

    def test_load_states(self):
        """Ensure states are loaded"""
        g = Game.TestGame(state_path="tests/states")
        self.assertEqual(g.states, {})
        game_setup.load_states(g)
        self.assertNotEqual(g.states, {})
        self.assertEqual(set(g.states.keys()), {"Unique", "NonUnique"})
        game_setup.load_states(g)  # Try loading again
        self.assertEqual(set(g.states.keys()), {"Unique", "NonUnique"})


###############################################################################
class TestLoadBoons(unittest.TestCase):
    """Test load_boons()"""

    def test_load_boons(self):
        """Ensure boons are loaded"""
        g = Game.TestGame(boon_path="tests/boons")
        self.assertEqual(g.boons, [])
        game_setup.load_boons(g)
        self.assertNotEqual(g.boons, [])
        self.assertEqual(g.boons[0].name, "TestBoon")
        game_setup.load_boons(g)
        self.assertNotEqual(g.boons, [])


###############################################################################
class TestLoadAlly(unittest.TestCase):
    """Test load_ally()"""

    def test_load_ally_by_name(self):
        """Ensure allies are loaded"""
        g = Game.TestGame(ally_path="tests/allies")
        self.assertEqual(g.boons, [])
        ally = game_setup.load_ally(g, "Noop")
        self.assertEqual(ally.name, "noop")

    def test_load_ally_by_list(self):
        """Ensure allies are loaded"""
        g = Game.TestGame(ally_path="tests/allies")
        self.assertEqual(g.boons, [])
        ally = game_setup.load_ally(g, ["Noop"])
        self.assertEqual(ally.name, "noop")


###############################################################################
class TestGetCardClasses(unittest.TestCase):
    """Test get_card_classes()"""

    def test_get_card_classes(self):
        """Test get_card_classes()"""
        card_classes = game_setup.get_card_classes("Ally", "tests/allies", "Ally_")
        self.assertEqual(list(card_classes.keys()), ["noop"])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

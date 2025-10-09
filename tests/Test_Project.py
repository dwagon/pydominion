#!/usr/bin/env python
"""http://wiki.dominionstrategy.com/index.php/Project"""

import unittest

from dominion import Game


###############################################################################
class Test_assignProject(unittest.TestCase):
    """Test assigning projects"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=2,
            initcards=["StateTester"],
            state_path="tests/states",
            card_path="tests/cards",
            numstacks=1,
            boon_path="tests/boons",
            project_path="tests/projects",
            projects=["ProjectA", "ProjectB", "ProjectC"],
        )
        self.g.start_game()
        self.plr, self.plr2 = self.g.player_list()

    def test_assign(self):
        """Simple assigning"""
        self.plr.assign_project("ProjectA")
        st = self.plr.projects[0]
        self.assertEqual(st.name, "ProjectA")

    def test_assign_twice(self):
        """Assign the same twice"""
        rc = self.plr.assign_project("ProjectA")
        self.assertTrue(rc)
        rc = self.plr.assign_project("ProjectA")
        self.assertFalse(rc)
        self.assertEqual(self.plr.projects[0].name, "ProjectA")
        self.assertEqual(len(self.plr.projects), 1)

    def test_assign_three(self):
        """Assign more than two projects"""
        rc = self.plr.assign_project("ProjectA")
        self.assertTrue(rc)
        rc = self.plr.assign_project("ProjectB")
        self.assertTrue(rc)
        rc = self.plr.assign_project("ProjectC")
        self.assertFalse(rc)
        self.assertEqual(len(self.plr.projects), 2)
        self.assertEqual(
            sorted([_.name for _ in self.plr.projects]),
            sorted(["ProjectA", "ProjectB"]),
        )

    def test_assign_two_plr(self):
        """Assign same project to two different players"""
        rc = self.plr.assign_project("ProjectA")
        self.assertTrue(rc)
        rc = self.plr2.assign_project("ProjectA")
        self.assertTrue(rc)


###############################################################################
class Test_buy_project(unittest.TestCase):
    """Test Buying a project"""

    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["StateTester"],
            state_path="tests/states",
            card_path="tests/cards",
            numstacks=1,
            boon_path="tests/boons",
            project_path="tests/projects",
            projects=["ProjectA"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_buy(self):
        """Test Buying a project"""
        PA = self.g.projects["ProjectA"]
        self.plr.buys.set(1)
        self.plr.coins.set(3)
        self.plr.buy_project(PA)
        self.assertEqual(self.plr.buys.get(), 0)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.projects[0].name, "ProjectA")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

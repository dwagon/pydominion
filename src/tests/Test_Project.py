#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_assignProject(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=2, initcards=['StateTester'],
            statepath='tests/states', cardpath='tests/cards', numstacks=1,
            boonpath='tests/boons', projectpath='tests/projects',
            initprojects=['ProjectA', 'ProjectB', 'ProjectC']
        )
        self.g.start_game()
        self.plr, self.plr2 = self.g.player_list()

    def test_assign(self):
        self.plr.assign_project('ProjectA')
        st = self.plr.projects[0]
        self.assertEqual(st.name, 'ProjectA')

    def test_assign_twice(self):
        rc = self.plr.assign_project('ProjectA')
        self.assertEqual(rc, True)
        rc = self.plr.assign_project('ProjectA')
        self.assertEqual(rc, False)
        self.assertEqual(self.plr.projects[0].name, 'ProjectA')
        self.assertEqual(len(self.plr.projects), 1)

    def test_assign_three(self):
        rc = self.plr.assign_project('ProjectA')
        self.assertEqual(rc, True)
        rc = self.plr.assign_project('ProjectB')
        self.assertEqual(rc, True)
        rc = self.plr.assign_project('ProjectC')
        self.assertEqual(rc, False)
        self.assertEqual(len(self.plr.projects), 2)
        self.assertEqual(sorted([_.name for _ in self.plr.projects]), sorted(['ProjectA', 'ProjectB']))

    def test_assign_two_plr(self):
        rc = self.plr.assign_project('ProjectA')
        self.assertEqual(rc, True)
        rc = self.plr2.assign_project('ProjectA')
        self.assertEqual(rc, True)


###############################################################################
class Test_buyProject(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=['StateTester'],
            statepath='tests/states', cardpath='tests/cards', numstacks=1,
            boonpath='tests/boons', projectpath='tests/projects',
            initprojects=['ProjectA']
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_buy(self):
        PA = self.g.projects['ProjectA']
        self.plr.setBuys(1)
        self.plr.setCoin(3)
        rc = self.plr.buyProject(PA)
        self.assertEqual(rc, True)
        self.assertEqual(self.plr.get_buys(), 0)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.projects[0].name, 'ProjectA')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

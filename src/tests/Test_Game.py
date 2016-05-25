#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_args(unittest.TestCase):
    def setUp(self):
        pass

    def test_numplayers(self):
        g = Game.Game(quiet=True, numplayers=4)
        g.startGame()
        self.assertEqual(len(g.playerList()), 4)

    def test_card(self):
        g = Game.Game(quiet=True, initcards=['Moat'])
        g.startGame()
        self.assertTrue('Moat' in g.cardpiles)

    def test_prosperity(self):
        g = Game.Game(quiet=True, prosperity=True)
        g.startGame()
        self.assertTrue('Colony' in g.cardpiles)
        self.assertTrue('Platinum' in g.cardpiles)


###############################################################################
class Test_game_over(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_not_over(self):
        """ The game isn't over yet """
        over = self.g.isGameOver()
        self.assertFalse(over)

    def test_provinces(self):
        """ Someone took the last province """
        for i in range(200):
            self.plr.gainCard('Province')
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_three_stacks(self):
        """ Three stacks are empty """
        for i in range(200):
            self.plr.gainCard('Estate')
            self.plr.gainCard('Copper')
            self.plr.gainCard('Silver')
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_two_stacks(self):
        """ Two stacks are empty """
        for i in range(200):
            self.plr.gainCard('Estate')
            self.plr.gainCard('Silver')
        over = self.g.isGameOver()
        self.assertFalse(over)


###############################################################################
class Test_inTrash(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.plr.setHand('Copper')
        self.plr.trashCard(self.plr.hand[0])

    def test_intrash(self):
        """ Test card is in trash """
        self.assertTrue(self.g.inTrash('Copper'))
        self.assertEqual(self.g.inTrash('Copper').name, 'Copper')

    def test_intrash_with_card(self):
        """ Test card is in trash passing a card """
        cu = self.g['Copper'].remove()
        self.assertTrue(self.g.inTrash(cu))
        self.assertEqual(self.g.inTrash(cu).name, 'Copper')

    def test_notintrash(self):
        """ Test card that isn't in trash """
        self.assertFalse(self.g.inTrash('Estate'))


###############################################################################
class Test_actionpiles(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.startGame()

    def test_actionpiles(self):
        piles = self.g.getActionPiles()
        self.assertIn(self.g.cardpiles['Moat'], piles)
        self.assertNotIn(self.g.cardpiles['Copper'], piles)


###############################################################################
class Test_whowon(unittest.TestCase):
    def setUp(self):
        self.numplayers = 3
        self.g = Game.Game(quiet=True, numplayers=self.numplayers)
        self.g.startGame()

    def test_whoWon(self):
        scores = self.g.whoWon()
        # Everyone should get 3 estates at start
        for score in scores.values():
            self.assertEqual(score, 3)
        self.assertEqual(len(scores), self.numplayers)


###############################################################################
class Test_parse_args(unittest.TestCase):
    def test_defaults(self):
        args = Game.parseArgs([])
        self.assertEqual(args.numplayers, 2)
        self.assertEqual(args.cardbase, None)
        self.assertEqual(args.prosperity, False)
        self.assertEqual(args.initcards, [])

    def test_prosperity(self):
        args = Game.parseArgs(['--prosperity'])
        self.assertEqual(args.prosperity, True)

    def test_numplayers(self):
        args = Game.parseArgs(['--numplayers', '4'])
        self.assertEqual(args.numplayers, 4)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

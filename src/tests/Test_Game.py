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
        self.assertIn('Moat', g.cardpiles)

    def test_prosperity(self):
        g = Game.Game(quiet=True, prosperity=True)
        g.startGame()
        self.assertIn('Colony', g.cardpiles)
        self.assertIn('Platinum', g.cardpiles)

    def test_event(self):
        """ Test that we can specify an event on the command line """
        g = Game.Game(quiet=True, eventcards=['Alms'])
        g.startGame()
        self.assertIn('Alms', g.events)


###############################################################################
class Test_guess_cardname(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2)
        self.g.startGame()

    def test_guesses(self):
        self.assertEqual(self.g.guess_cardname('moat'), 'Moat')
        self.assertEqual(self.g.guess_cardname('grandmarket'), 'Grand Market')
        self.assertEqual(self.g.guess_cardname('philosophersstone'), "Philosopher's Stone")
        self.assertIsNone(self.g.guess_cardname('nosuchcard'))


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
        while(self.g['Province'].numcards):
            self.plr.gainCard('Province')
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_three_stacks(self):
        """ Three stacks are empty """
        while(self.g['Estate'].numcards):
            self.plr.gainCard('Estate')
        while(self.g['Copper'].numcards):
            self.plr.gainCard('Copper')
        while(self.g['Silver'].numcards):
            self.plr.gainCard('Silver')
        over = self.g.isGameOver()
        self.assertTrue(over)

    def test_two_stacks(self):
        """ Two stacks are empty """
        while(self.g['Estate'].numcards):
            self.plr.gainCard('Estate')
        while(self.g['Silver'].numcards):
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
class Test_boon(unittest.TestCase):
    # TODO - convert to using real boons rather than letters
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1)
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_receive_boon_empty(self):
        self.g.boons = []
        self.g.discarded_boons = ['a', 'b', 'c', 'd']
        b = self.g.receive_boon()
        self.assertIn(b, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.g.discarded_boons, [])
        self.assertEqual(len(self.g.boons), 3)
        self.assertNotIn(b, self.g.boons)

    def test_receive_boon_non_empty(self):
        self.g.boons = ['a', 'b']
        self.g.discarded_boons = ['c', 'd']
        b = self.g.receive_boon()
        self.assertIn(b, ['a', 'b'])
        self.assertEqual(self.g.discarded_boons, ['c', 'd'])
        self.assertEqual(len(self.g.boons), 1)
        self.assertNotIn(b, self.g.boons)

    def test_discard_boon(self):
        # TODO
        return
        self.g.boons = ['b']
        self.g.discarded_boons = ['c', 'd']
        self.g.discard_boon('a')
        self.assertEqual(self.g.discarded_boons, ['c', 'd', 'a'])
        self.assertEqual(self.g.boons, ['b'])


###############################################################################
class Test_whowon(unittest.TestCase):
    def setUp(self):
        self.numplayers = 3
        self.g = Game.Game(quiet=True, numplayers=self.numplayers, badcards=['Shepherd'])
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

    def test_events(self):
        args = Game.parseArgs(['--events', 'Alms'])
        self.assertEqual(args.eventcards, ['Alms'])

    def test_use_events(self):
        args = Game.parseArgs(['--quiet', '--events', 'Alms'])
        g = Game.Game(**vars(args))
        g.startGame()
        self.assertIn('Alms', g.events)

    def test_use_card(self):
        args = Game.parseArgs(['--quiet', '--card', 'Moat'])
        g = Game.Game(**vars(args))
        g.startGame()
        self.assertIn('Moat', g.cardpiles)

    def test_use_landmark(self):
        args = Game.parseArgs(['--quiet', '--landmark', 'Aqueduct'])
        g = Game.Game(**vars(args))
        g.startGame()
        self.assertIn('Aqueduct', g.landmarks)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

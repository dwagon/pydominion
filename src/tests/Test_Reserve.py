#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_getWhens(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_start(self):
        self.plr.startTurn()
        whens = self.plr.getWhens()
        self.assertEquals(whens, ['any', 'start'])

    def test_not_start(self):
        self.plr.startTurn()
        self.plr.perform_action({'action': 'spendall'})
        whens = self.plr.getWhens()
        self.assertNotIn('start', whens)

    def test_any(self):
        whens = self.plr.getWhens()
        self.assertIn('any', whens)

    def test_postaction(self):
        self.plr.setPlayed('Moat')
        whens = self.plr.getWhens()
        self.assertIn('postaction', whens)
        self.plr.setPlayed('Copper')
        whens = self.plr.getWhens()
        self.assertNotIn('postaction', whens)

    def test_not_postaction(self):
        whens = self.plr.getWhens()
        self.assertNotIn('postaction', whens)
        self.plr.perform_action({'action': 'spendall'})
        whens = self.plr.getWhens()
        self.assertNotIn('postaction', whens)


###############################################################################
class Test_Reserve(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Coin of the Realm'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_inreserve(self):
        """ Test inReserve() """
        self.plr.setReserve('Copper')
        self.assertTrue(self.plr.inReserve('Copper'))
        self.assertEqual(self.plr.inReserve('Copper').name, 'Copper')

    def test_not_inreserve(self):
        """ Test inReserve() """
        self.plr.setReserve('Copper')
        self.assertFalse(self.plr.inReserve('Estate'))

    def test_setReserve(self):
        """ set reserved """
        self.plr.setReserve('Silver')
        self.assertEqual(self.plr.reserveSize(), 1)
        self.assertEqual(self.plr.reserve[0].name, 'Silver')

    def test_callReserve(self):
        self.plr.setReserve('Silver')
        self.assertEquals(self.plr.reserveSize(), 1)
        c = self.plr.callReserve('Silver')
        self.assertEquals(self.plr.reserveSize(), 0)
        self.assertEquals(c.name, 'Silver')

    def test_bad_callReserve(self):
        self.plr.setReserve('Copper')
        c = self.plr.callReserve('Silver')
        self.assertIsNone(c)

    def test_addcard_reserve(self):
        gold = self.g['Gold'].remove()
        self.plr.addCard(gold, 'reserve')
        self.assertEqual(self.plr.reserveSize(), 1)
        self.assertEqual(self.plr.reserve[0].name, 'Gold')

    def test_isreserve(self):
        gold = self.g['Gold'].remove()
        self.assertFalse(gold.isReserve())
        cotr = self.g['Coin of the Realm'].remove()
        self.assertTrue(cotr.isReserve())


###############################################################################
class Test_reserveSelection(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Coin of the Realm'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_callable(self):
        gold = self.g['Gold'].remove()
        self.plr.addCard(gold, 'reserve')
        output, index = self.plr.reserveSelection(1)
        self.assertEquals(len(output), 1)
        self.assertEquals(output[0]['action'], 'reserve')
        self.assertEquals(output[0]['card'], gold)
        self.assertEquals(output[0]['selector'], 'b')
        self.assertEquals(index, 2)

    def test_not_callable(self):
        """ Copper is not callable (Due to miser) """
        copper = self.g['Copper'].remove()
        self.plr.addCard(copper, 'reserve')
        output, index = self.plr.reserveSelection(1)
        self.assertEquals(len(output), 0)
        self.assertEquals(index, 1)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

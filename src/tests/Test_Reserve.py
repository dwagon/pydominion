#!/usr/bin/env python

import unittest
import Game


###############################################################################
class Test_Reserve(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['coinoftherealm'])
        self.g.startGame()
        self.plr = self.g.playerList(0)

    def test_inreserve(self):
        """ Test inReserve() """
        self.plr.setReserve('copper')
        self.assertTrue(self.plr.inReserve('Copper'))
        self.assertEqual(self.plr.inReserve('Copper').name, 'Copper')

    def test_not_inreserve(self):
        """ Test inReserve() """
        self.plr.setReserve('copper')
        self.assertFalse(self.plr.inReserve('Estate'))

    def test_inreserve_card(self):
        """ Test inReserve() passing a card  """
        copper = self.g['copper'].remove()
        self.plr.setReserve('copper')
        self.assertTrue(self.plr.inReserve(copper))

    def test_setReserve(self):
        """ set reserved """
        self.plr.setReserve('silver')
        self.assertEqual(self.plr.reserveSize(), 1)
        self.assertEqual(self.plr.reserve[0].name, 'Silver')

    def test_callReserve(self):
        self.plr.setReserve('silver')
        self.assertEquals(self.plr.reserveSize(), 1)
        c = self.plr.callReserve('silver')
        self.assertEquals(self.plr.reserveSize(), 0)
        self.assertEquals(c.name, 'Silver')

    def test_bad_callReserve(self):
        self.plr.setReserve('copper')
        c = self.plr.callReserve('silver')
        self.assertIsNone(c)

    def test_addcard_reserve(self):
        gold = self.g['gold'].remove()
        self.plr.addCard(gold, 'reserve')
        self.assertEqual(self.plr.reserveSize(), 1)
        self.assertEqual(self.plr.reserve[0].name, 'Gold')

    def test_isreserve(self):
        gold = self.g['gold'].remove()
        self.assertFalse(gold.isReserve())
        cotr = self.g['coinoftherealm'].remove()
        self.assertTrue(cotr.isReserve())

    def test_reserveSelection(self):
        gold = self.g['gold'].remove()
        self.plr.addCard(gold, 'reserve')
        output, index = self.plr.reserveSelection(1)
        self.assertEquals(len(output), 1)
        self.assertEquals(output[0]['action'], 'reserve')
        self.assertEquals(output[0]['card'], gold)
        self.assertEquals(output[0]['selector'], 'b')
        self.assertEquals(index, 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

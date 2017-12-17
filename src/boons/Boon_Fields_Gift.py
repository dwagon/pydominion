#!/usr/bin/env python

import unittest
from Boon import Boon


###############################################################################
class Boon_Fields_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocture'
        self.desc = "+1 Action; +1 Coin"
        self.name = "The Field's Gift"
        self.purchasable = False
        self.coin = 1
        self.action = 1
        self.retain_boon = True


###############################################################################
class Test_Fields_Gift(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Page', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Champion'].remove()

    def test_champion(self):
        """ Play a champion """
        self.plr.addCard(self.card, 'duration')
        self.assertEqual(self.plr.getActions(), 1)
        moat = self.g['Moat'].remove()
        self.plr.addCard(moat, 'hand')
        self.plr.playCard(moat)
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

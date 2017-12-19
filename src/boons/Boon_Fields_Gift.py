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
        self.actions = 1
        self.retain_boon = True


###############################################################################
class Test_Fields_Gift(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for b in self.g.boons[:]:
            if b.name != "The Field's Gift":
                self.g.discarded_boons.append(b)
                self.g.boons.remove(b)
        self.card = self.g['Bard'].remove()

    def test_fields_gift(self):
        self.plr.coin = 0
        self.plr.action = 0
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1 + 2)     # Boon + Bard
        self.assertEqual(self.plr.getActions(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
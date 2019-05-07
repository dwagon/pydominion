#!/usr/bin/env python

import unittest
from Boon import Boon


###############################################################################
class Boon_Fields_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocturne'
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for b in self.g.boons:
            if b.name == "The Field's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_fields_gift(self):
        self.plr.coin = 0
        self.plr.action = 0
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.getCoin(), 1 + 2)     # Boon + Bard
            self.assertEqual(self.plr.getActions(), 1)
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

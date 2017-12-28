#!/usr/bin/env python

import unittest
from Boon import Boon


###############################################################################
class Boon_Mountains_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocture'
        self.desc = "Gain a silver"
        self.name = "The Mountain's Gift"
        self.purchasable = False

    def special(self, game, player):
        player.gainCard('Silver')


###############################################################################
class Test_Mountains_Gift(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for b in self.g.boons[:]:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break
        self.card = self.g['Bard'].remove()

    def test_mountains_gift(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

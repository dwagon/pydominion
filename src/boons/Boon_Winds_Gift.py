#!/usr/bin/env python

import unittest
from Boon import Boon


###############################################################################
class Boon_Winds_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocture'
        self.desc = "+2 Cards; Discard 2 cards."
        self.name = "The Wind's Gift"
        self.cards = 2
        self.purchasable = False

    def special(self, game, player):
        player.plrDiscardCards(num=2)


###############################################################################
class Test_Winds_Gift(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for b in self.g.boons[:]:
            if b.name == "The Wind's Gift":
                self.g.boons = [b]
        self.card = self.g['Bard'].remove()

    def test_winds_gift(self):
        self.plr.setHand('Duchy', 'Gold', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Duchy', 'Gold', 'Finish']
        self.plr.playCard(self.card)
        try:
            self.assertEqual(self.plr.handSize(), 3)
            self.assertIsNotNone(self.plr.inDiscard('Duchy'))
        except AssertionError:
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

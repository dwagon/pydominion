#!/usr/bin/env python

import unittest
from Boon import Boon


###############################################################################
class Boon_Skys_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocture'
        self.desc = "You may discard 3 cards to gain a Gold."
        self.name = "The Sky's Gift"
        self.purchasable = False

    def special(self, game, player):
        dc = player.plrDiscardCards(anynum=True, prompt="Discard 3 cards to gain a Gold")
        if len(dc) >= 3:
            player.gainCard('Gold')


###############################################################################
class Test_Skys_Gift(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        for b in self.g.boons[:]:
            if b.name != "The Sky's Gift":
                self.g.discarded_boons.append(b)
                self.g.boons.remove(b)
        self.card = self.g['Bard'].remove()

    def test_skys_gift(self):
        """ Discard 3 cards to gain a gold """
        self.plr.setHand('Copper', 'Estate', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper', 'Estate', 'Duchy', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertIsNotNone(self.plr.inDiscard('Gold'))

    def test_skys_no_gift(self):
        """ Discard less than three cards to gain nothing """
        self.plr.setHand('Copper', 'Estate', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper', 'Estate', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertIsNone(self.plr.inDiscard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

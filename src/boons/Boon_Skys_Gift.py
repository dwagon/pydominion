#!/usr/bin/env python

import unittest
import Card
import Game
from Boon import Boon


###############################################################################
class Boon_Skys_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = Card.TYPE_BOON
        self.base = Game.NOCTURNE
        self.desc = "You may discard 3 cards to gain a Gold."
        self.name = "The Sky's Gift"
        self.purchasable = False

    def special(self, game, player):
        dc = player.plrDiscardCards(anynum=True, prompt="Discard 3 cards to gain a Gold")
        if len(dc) >= 3:
            player.gainCard('Gold')
            player.output("Gained a Gold")


###############################################################################
class Test_Skys_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Sky's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_skys_gift(self):
        """ Discard 3 cards to gain a gold """
        self.plr.setHand('Copper', 'Estate', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper', 'Estate', 'Duchy', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertIsNotNone(self.plr.in_discard('Gold'))

    def test_skys_no_gift(self):
        """ Discard less than three cards to gain nothing """
        self.plr.setHand('Copper', 'Estate', 'Duchy', 'Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Copper', 'Estate', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 2)
        self.assertIsNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

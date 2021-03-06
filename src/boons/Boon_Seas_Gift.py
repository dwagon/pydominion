#!/usr/bin/env python

import unittest
import Card
import Game
from Boon import Boon


###############################################################################
class Boon_Seas_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = Card.TYPE_BOON
        self.base = Game.NOCTURNE
        self.desc = "+1 Card"
        self.name = "The Sea's Gift"
        self.purchasable = False
        self.cards = 1


###############################################################################
class Test_Seas_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Sea's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_seas_gift(self):
        self.plr.setHand('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

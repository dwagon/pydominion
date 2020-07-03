#!/usr/bin/env python

import unittest
import Game
from Boon import Boon


###############################################################################
class Boon_Rivers_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = 'boon'
        self.base = 'nocturne'
        self.desc = "+1 Card at the end of this turn."
        self.name = "The River's Gift"
        self.purchasable = False

    def special(self, game, player):
        player.newhandsize += 1


###############################################################################
class Test_Rivers_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The River's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_winds_gift(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.end_turn()
        self.assertEqual(self.plr.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

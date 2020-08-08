#!/usr/bin/env python

import unittest
import Game
from Boon import Boon


###############################################################################
class Boon_Flames_Gift(Boon):
    def __init__(self):
        Boon.__init__(self)
        self.cardtype = Card.BOON
        self.base = Game.NOCTURNE
        self.desc = "You may trash a card from your hand"
        self.name = "The Flame's Gift"
        self.purchasable = False

    def special(self, game, player):
        player.plrTrashCard()


###############################################################################
class Test_Flames_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Flame's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g['Bard'].remove()

    def test_flames_gift(self):
        self.plr.setHand('Duchy')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Duchy']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Duchy'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

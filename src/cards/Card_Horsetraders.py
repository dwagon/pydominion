#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Horsetraders(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reaction']
        self.base = 'cornucopia'
        self.desc = """+1 Buy. +3 Coins. Discard 2 cards.
        When another player plays an Attack card, you may set this aside from your hand.
        If you do, then at the start of your next turn, +1 Card and return this to your hand."""
        self.name = 'Horse Traders'
        self.buys = 1
        self.coin = 3
        self.cost = 4

    def special(self, game, player):
        player.plrDiscardCards(num=2)

    def todo(self):     # TODO
        """ When another player plays an Attack card, you may set
        this aside from your hand.  If you do, then at the start
        of your next turn, +1 Card and return this to your hand. """


###############################################################################
class Test_Horsetraders(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Horse Traders'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Horse Traders'].remove()

    def test_play(self):
        self.plr.setHand('Estate', 'Duchy', 'Province')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Estate', 'Duchy', 'Finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 3)
        self.assertEqual(self.plr.discardSize(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

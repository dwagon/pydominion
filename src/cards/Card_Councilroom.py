#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Councilroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DOMINION
        self.desc = "+4 cards, +1 buy. Everyone else +1 card"
        self.name = 'Council Room'
        self.cards = 4
        self.buys = 1
        self.cost = 5

    def special(self, game, player):
        """ Each other player draws a card """
        for pl in game.player_list():
            if pl != player:
                pl.output("Picking up card due to %s playing a Council Room" % player.name)
                pl.pickupCard()


###############################################################################
class Test_Councilroom(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Council Room'])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.ccard = self.g['Council Room'].remove()
        self.plr.addCard(self.ccard, 'hand')

    def test_play(self):
        self.assertEqual(self.other.handSize(), 5)
        self.plr.playCard(self.ccard)
        self.assertEqual(self.other.handSize(), 6)
        self.assertEqual(self.plr.handSize(), 9)
        self.assertEqual(self.plr.getBuys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

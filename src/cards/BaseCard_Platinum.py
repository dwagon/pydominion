#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Platinum(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.PROSPERITY
        self.desc = "+5 coin"
        self.name = 'Platinum'
        self.playable = False
        self.basecard = True
        self.coin = 5
        self.cost = 9
        self.numcards = 12


###############################################################################
class Test_Platinum(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, prosperity=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Platinum'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a platinum """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

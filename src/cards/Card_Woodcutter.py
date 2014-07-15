#!/usr/bin/env python

import unittest
from Card import Card


class Card_Woodcutter(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 buys, +2 coin"
        self.name = 'Woodcutter'
        self.buys = 1
        self.coin = 2
        self.cost = 3


###############################################################################
class Test_Woodcutter(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['woodcutter'])
        self.plr = list(self.g.players.values())[0]
        self.card = self.g['woodcutter'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the woodcutter """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.getBuys(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

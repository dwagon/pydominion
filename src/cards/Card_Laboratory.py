#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Laboratory(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+2 cards, +1 action"
        self.name = 'Laboratory'
        self.cards = 2
        self.actions = 1
        self.cost = 5


###############################################################################
class Test_Laboratory(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['laboratory'])
        self.plr = self.g.players[0]
        self.card = self.g['laboratory'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Laboratory """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.t['actions'], 1)
        # 5 hand, +2 for playing lab
        self.assertEqual(len(self.plr.hand), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

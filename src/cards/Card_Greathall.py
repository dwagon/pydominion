#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Greathall(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'intrigue'
        self.desc = "+1 card, +1 action, 1VP"
        self.name = 'Great Hall'
        self.cost = 3
        self.cards = 1
        self.actions = 1

    def special_score(self, game, player):
        return 1


###############################################################################
class Test_Greathall(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['greathall'])
        self.plr = self.g.players[0]
        self.card = self.g['greathall'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Great Hall """
        self.plr.playCard(self.card)
        self.assertEqual(len(self.plr.hand), 6)
        self.assertEqual(self.plr.t['actions'], 1)

    def test_score(self):
        """ Have a victory point just for existing """
        score = self.plr.getScoreDetails()
        self.assertEqual(score['Great Hall'], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

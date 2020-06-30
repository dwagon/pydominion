#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Fishingvillage(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.base = 'seaside'
        self.desc = "+1 coin, +2 actions; next turn +1 coin, +1 action"
        self.name = 'Fishing Village'
        self.coin = 1
        self.actions = 2
        self.cost = 3

    def duration(self, game, player):
        """ +1 action, +1 coin"""
        player.addCoin(1)
        player.addActions(1)


###############################################################################
class Test_Fishingvillage(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Fishing Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Fishing Village'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a fishing village """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.durationSize(), 1)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.durationSize(), 0)
        self.assertEqual(self.plr.playedSize(), 1)
        self.assertEqual(self.plr.played[-1].name, 'Fishing Village')
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

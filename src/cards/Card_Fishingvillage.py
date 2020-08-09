#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_Fishingvillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.ACTION, Card.DURATION]
        self.base = Game.SEASIDE
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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Fishing Village'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Fishing Village'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_playcard(self):
        """ Play a fishing village """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.durationSize(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.durationSize(), 0)
        self.assertEqual(self.plr.played_size(), 1)
        self.assertEqual(self.plr.played[-1].name, 'Fishing Village')
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

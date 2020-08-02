#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Peasant(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'traveller']
        self.base = 'adventure'
        self.desc = "+1 Buy, +1 Coin; Discard to replace with Soldier"
        self.name = 'Peasant'
        self.traveller = True
        self.buys = 1
        self.coin = 1
        self.cost = 2

    def hook_discardThisCard(self, game, player, source):
        """ Replace with Treasure Hunter """
        player.replace_traveller(self, 'Soldier')


###############################################################################
class Test_Peasant(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Peasant'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Peasant'].remove()

    def test_play(self):
        """ Play a peasant """
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

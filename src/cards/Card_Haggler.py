#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Haggler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'hinterlands'
        self.desc = "+2 Coin. While this is in play, when you buy a card, gain a card costing less than it that is not a Victory card."
        self.name = 'Haggler'
        self.coin = 2
        self.cost = 5

    def hook_buyCard(self, game, player, card):
        cost = card.cost - 1
        player.plrGainCard(cost=cost, types={'action': True, 'treasure': True}, prompt="Gain a non-Victory card costing under %s" % cost)


###############################################################################
class Test_Haggler(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Haggler'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Haggler'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_buy(self):
        """ Buy a Gold and haggle a silver """
        self.plr.setPlayed('Haggler')
        self.plr.test_input = ['Get Silver']
        self.plr.setCoin(6)
        self.plr.buyCard(self.g['Gold'])
        self.assertIsNotNone(self.plr.in_discard('Silver'))
        self.assertIsNotNone(self.plr.in_discard('Gold'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

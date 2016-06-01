#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Winemerchant(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reserve']
        self.base = 'adventure'
        self.desc = """+1 Buy, +4 Coin; At the end of your Buy phase, if you have at least 2 Coin unspent, you may discard this from your Tavern mat."""
        self.name = 'Wine Merchant'
        self.buys = 1
        self.coin = 4
        self.cost = 5
        self.callable = False

    def hook_endTurn(self, game, player):
        if player.coin >= 2:
            player.output("Discarding Wine Merchant")
            player.reserve.remove(self)
            player.addCard(self, 'discard')


###############################################################################
class Test_Winemerchant(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Wine Merchant'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Wine Merchant'].remove()

    def test_play(self):
        """ Play a Wine Merchant """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 2)
        self.assertEqual(self.plr.getCoin(), 4)

    def test_recover(self):
        """ Recover a wine merchant """
        self.plr.coin = 2
        self.plr.setReserve('Wine Merchant')
        self.plr.test_input = ['end phase', 'end phase']
        self.plr.turn()
        self.assertEqual(self.plr.reserveSize(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

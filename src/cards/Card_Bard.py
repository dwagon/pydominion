#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Bard(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'fate']
        self.base = 'nocturne'
        self.desc = "+2 Coin; Receive a boon"
        self.name = 'Bard'
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        player.receive_boon()


###############################################################################
class Test_Bard(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.bard = self.g['Bard'].remove()

    def test_play_card(self):
        """ Play Bard """
        self.coin = 0
        self.plr.setHand('Duchy')
        self.plr.addCard(self.bard, 'hand')
        self.plr.gainCard('Silver')
        self.plr.test_input = ['Duchy']
        self.plr.playCard(self.bard)
        self.assertGreaterEqual(self.plr.getCoin(), 2)  # 2 for bard +x for boon


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

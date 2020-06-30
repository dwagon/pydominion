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
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Bard'], badcards=['Druid'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.bard = self.g['Bard'].remove()
        for b in self.g.boons[:]:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break

    def test_play_card(self):
        """ Play Bard """
        self.plr.addCard(self.bard, 'hand')
        self.plr.playCard(self.bard)
        self.assertGreaterEqual(self.plr.getCoin(), 2)
        # Check boon happened
        self.assertIsNotNone(self.plr.inDiscard('Silver'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

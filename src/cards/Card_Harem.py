#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Harem(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'victory']
        self.base = 'intrigue'
        self.name = 'Harem'
        self.coin = 2
        self.victory = 2
        self.cost = 6

    def desc(self, player):
        if player.phase == "buy":
            return "+2 coin; 2 VPs"
        else:
            return "+2 coin"


###############################################################################
class Test_Harem(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Harem'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Harem'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play a Harem """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 2)

    def test_score(self):
        """ Score the harem """
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc['Harem'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

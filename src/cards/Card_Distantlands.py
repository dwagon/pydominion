#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Distantlands(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'reserve', 'victory']
        self.base = 'adventure'
        self.desc = "Worth 4 VP if on your tavern mat at the end of the game, else 0"
        self.name = 'Distant Lands'
        self.cost = 5
        self.callable = False
        self.counted = False

    def special_score(self, game, player):
        """ Worth 4 VP if on your tavern mat; else 0"""
        score = 0
        if game.gameover:
            for c in player.reserve:
                if c.name == 'Distant Lands' and not c.counted:
                    c.counted = True
                    score += 4
        return score


###############################################################################
class Test_Distantlands(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Distant Lands'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Distant Lands'].remove()

    def test_play(self):
        """ Play a distant lands"""
        self.plr.setHand()
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.reserveSize(), 1)
        self.assertIsNotNone(self.plr.in_reserve('Distant Lands'))

    def test_notonmat(self):
        self.plr.setHand('Distant Lands')
        self.g.gameover = True
        self.assertEqual(self.plr.getScoreDetails()['Distant Lands'], 0)

    def test_onmat(self):
        """ Distant lands on mat """
        self.plr.setReserve('Distant Lands')
        self.g.gameover = True
        self.assertEqual(self.plr.getScoreDetails()['Distant Lands'], 4)

    def test_onmat_twice(self):
        """ Two Distant lands on mat """
        self.plr.setReserve('Distant Lands', 'Distant Lands')
        self.g.gameover = True
        self.assertEqual(self.plr.getScoreDetails()['Distant Lands'], 8)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

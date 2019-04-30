#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Inventor(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'renaissance'
        self.desc = "Gain a card costing up to 4, then cards cost 1 less this turn (but not less than 0)."
        self.name = 'Inventor'
        self.cost = 4

    def special(self, game, player):
        """ Gain a card costing up to 4"""
        player.plrGainCard(4)

    def hook_cardCost(self, game, player, card):
        if self in player.played:
            return -1
        return 0


###############################################################################
class Test_Inventor(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Inventor', 'Feast'], badcards=['Blessed Village', 'Cemetery'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.inventor = self.g['Inventor'].remove()
        self.plr.addCard(self.inventor, 'hand')

    def test_play(self):
        self.plr.test_input = ['Get Feast']
        self.assertEqual(self.plr.cardCost(self.g['Gold']), 6)
        self.plr.playCard(self.inventor)
        self.assertEqual(self.plr.cardCost(self.g['Gold']), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

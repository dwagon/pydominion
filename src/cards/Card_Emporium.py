#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Emporium(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'empires'
        self.desc = "+1 Card, +1 Action, +1 Coin. When you gain this, if you have at least 5 Action cards in play, +2VP."
        self.name = 'Emporium'
        self.coin = 1
        self.actions = 1
        self.cards = 1
        self.cost = 5

    ###########################################################################
    def hook_gainThisCard(self, game, player):
        count = sum([1 for c in player.played if c.isAction()])
        if count >= 5:
            player.addScore('Emporium', 2)


###############################################################################
class Test_Emporium(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Emporium', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Emporium'].remove()

    def test_play(self):
        """ Play the Emporium """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 1)

    def test_gain_with_actions(self):
        """ Play the Emporium having played lots of actions"""
        self.plr.setPlayed('Moat', 'Moat', 'Moat', 'Moat', 'Moat')
        self.plr.gainCard('Emporium')
        self.assertEqual(self.plr.getScoreDetails()['Emporium'], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

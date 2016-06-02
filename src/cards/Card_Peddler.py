#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Peddler(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "+1 Card, +1 Action, +1 Coin. During your Buy phase, this costs 2 less per Action card you have in play, but not less than 0"
        self.name = 'Peddler'
        self.cards = 1
        self.actions = 1
        self.coin = 1
        self.cost = 8

    def hook_thisCardCost(self, game, player):
        cost = 0
        for card in player.played:
            if card.isAction():
                cost -= 2
        return max(cost, -8)


###############################################################################
class Test_Peddler(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Peddler', 'Moat'])
        self.g.startGame()
        self.plr = self.g.playerList()[0]
        self.card = self.g['Peddler'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 5 + 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.getActions(), 1)

    def test_buy(self):
        self.plr.setPlayed('Moat')
        cost = self.plr.cardCost(self.card)
        self.assertEqual(cost, 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

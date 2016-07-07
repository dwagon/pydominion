#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Lighthouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['action', 'duration']
        self.desc = """+1 Action. Now and at the start of your next turn: +1 Coin.
        While this is in play, when another player plays an Attack card, it doesn't affect you."""
        self.name = 'Lighthouse'
        self.base = 'seaside'
        self.defense = True
        self.actions = 1
        self.cost = 2

    def duration(self, game, player):
        player.addCoin(1)

    def special(self, game, player):
        player.addCoin(1)


###############################################################################
class Test_Lighthouse(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Lighthouse'])
        self.g.startGame()
        self.plr, self.vic = self.g.playerList()
        self.card = self.g['Lighthouse'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.getActions(), 1)
        self.assertEqual(self.plr.getCoin(), 1)
        self.plr.endTurn()
        self.plr.startTurn()
        self.assertEqual(self.plr.getCoin(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
#!/usr/bin/env python

import unittest
from Card import Card


class Card_Village(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 cards, +2 actions"
        self.name = 'Village'
        self.cards = 1
        self.actions = 2
        self.cost = 3


###############################################################################
class Test_Village(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['village'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['village'].remove()
        self.plr.addCard(self.card, 'hand')

    def test_play(self):
        """ Play the village """
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.handSize(), 6)
        self.assertEqual(self.plr.getActions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

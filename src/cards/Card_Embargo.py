#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Embargo(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'seaside'
        self.desc = """+2 Coin. Trash this card. Put an Embargo token on top of a Supply pile.
        When a player buys a card, he gains a Curse card per Embargo token on that pile."""
        self.name = 'Embargo'
        self.coin = 2
        self.cost = 2

    def special(self, game, player):
        pass    # TODO


###############################################################################
class Test_Embargo(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Embargo'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Embargo'].remove()

    def test_play(self):
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

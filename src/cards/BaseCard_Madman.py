#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Madman(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'darkages'
        self.desc = """+2 Actions. Return this to the Madman pile. If you do, +1 Card per card in your hand."""
        self.name = 'Madman'
        self.actions = 2
        self.cost = 0
        self.purchasable = False

    def special(self, game, player):
        handsize = player.handSize()
        player.output("Gaining %d cards from madman" % handsize)
        for i in range(handsize):
            player.pickupCard()
        game['Madman'].add()
        player.played.remove(self)


###############################################################################
class Test_Madman(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Hermit'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.card = self.g['Madman'].remove()

    def test_play(self):
        """ Play a Madman """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.getActions(), 2)
        self.assertEqual(self.plr.handSize(), 5 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

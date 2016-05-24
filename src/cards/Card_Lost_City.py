#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Lost_City(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'adventure'
        self.desc = "+2 Cards, +2 Actions; When you gain this every else gains a card"
        self.name = 'Lost City'
        self.cards = 2
        self.actions = 2
        self.cost = 5

    def special(self, game, player):
        """ When you gain this, each other player draws a card """
        for pl in game.playerList():
            if pl != player:
                c = pl.pickupCard()
                pl.output("Picking up a %s due to %s playing a List City" % (c.name, player.name))


###############################################################################
class Test_Lost_City(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=2, initcards=['Lost City'])
        self.g.startGame()
        self.plr, self.other = self.g.playerList()
        self.card = self.g['Lost City'].remove()

    def test_play(self):
        """ Play a lost_city """
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.g.print_state()
        self.assertEqual(self.plr.handSize(), 5 + 2)
        self.assertTrue(self.other.handSize(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

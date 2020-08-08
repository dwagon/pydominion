#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Countinghouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.PROSPERITY
        self.desc = """Look through the discard pile, reveal any number of
            copper cards from it, and put them into your hand."""
        self.name = 'Counting House'
        self.cost = 5

    def special(self, game, player):
        count = 0
        for c in player.discardpile:
            if c.name == 'Copper':
                player.addCard(c, 'hand')
                player.discardpile.remove(c)
                count += 1
        player.output("Picked up %d coppers" % count)


###############################################################################
class Test_Countinghouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Counting House'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ch = self.g['Counting House'].remove()
        self.plr.setHand()
        self.plr.addCard(self.ch, 'hand')

    def test_pullcoppers(self):
        self.plr.setDiscard('Copper', 'Gold', 'Duchy', 'Copper')
        self.plr.playCard(self.ch)
        self.assertEqual(self.plr.handSize(), 2)
        for c in self.plr.hand:
            self.assertEqual(c.name, 'Copper')
        for c in self.plr.discardpile:
            self.assertNotEqual(c.name, 'Copper')


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

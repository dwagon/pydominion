#!/usr/bin/env python

import unittest
from Card import Card


class Card_Countinghouse(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'prosperity'
        self.desc = "Pull coppers out of discard"
        self.name = 'Counting House'
        self.cost = 5

    def special(self, game, player):
        """ Look through the discard pile, reveal any number of
            copper cards from it, and put them into your hand """
        count = 0
        for c in player.discardpile:
            if c.cardname == 'copper':
                player.addCard(c, 'hand')
                player.discardpile.remove(c)
                count += 1
        player.output("Picked up %d coppers" % count)


###############################################################################
class Test_Countinghouse(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['countinghouse'])
        self.g.startGame()
        self.plr = self.g.playerList(0)
        self.ch = self.g['countinghouse'].remove()
        self.plr.setHand()
        self.plr.addCard(self.ch, 'hand')

    def test_pullcoppers(self):
        self.plr.setDiscard('copper', 'gold', 'duchy', 'copper')
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

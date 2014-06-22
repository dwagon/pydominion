#!/usr/bin/env python

import unittest
from Card import Card


class Card_Councilroom(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+4 cards, +1 buy. Everyone else +1 card"
        self.name = 'Council Room'
        self.cards = 4
        self.buys = 1
        self.cost = 5

    def special(self, game, player):
        """ Each other player draws a card """
        for pl in game.players.values():
            if pl != player:
                pl.output("Picking up card due to %s playing a councilroom" % player.name)
                pl.pickupCard()


###############################################################################
class Test_Councilroom(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=2, initcards=['councilroom'])
        self.plr, self.other = self.g.players.values()
        self.ccard = self.g['councilroom'].remove()
        self.plr.addCard(self.ccard, 'hand')

    def test_play(self):
        self.assertEquals(len(self.other.hand), 5)
        self.plr.playCard(self.ccard)
        self.assertEquals(len(self.other.hand), 6)
        self.assertEquals(len(self.plr.hand), 9)
        self.assertEquals(self.plr.getBuys(), 2)

###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

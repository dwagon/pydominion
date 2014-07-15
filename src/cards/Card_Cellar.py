#!/usr/bin/env python

import unittest
from Card import Card


###############################################################################
class Card_Cellar(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "+1 action, Discard and redraw cards"
        self.name = 'Cellar'
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        """ Discard any number of cards, +1 card per card discarded """
        todiscard = player.plrDiscardCards(0, anynum=True)
        player.pickupCards(len(todiscard))


###############################################################################
class Test_Cellar(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['cellar'])
        self.plr = self.g.players.values()[0]
        self.ccard = self.g['cellar'].remove()

    def test_none(self):
        self.plr.setHand('estate', 'copper', 'silver')
        self.plr.addCard(self.ccard, 'hand')
        self.plr.test_input = ['finish']
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.handSize(), 3)

    def test_one(self):
        self.plr.setHand('estate', 'copper', 'silver')
        self.plr.setDeck('province', 'gold')
        self.plr.addCard(self.ccard, 'hand')
        self.plr.test_input = ['discard estate', 'finish']
        self.plr.playCard(self.ccard)
        self.assertEquals(self.plr.deck[-1].name, 'Province')
        for c in self.plr.hand:
            if c.name == 'Gold':
                break
        else:   # pragma: no cover
            self.fail()
        self.assertEquals(self.plr.handSize(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

#!/usr/bin/env python

import unittest
import Game
from Card import Card


class Card_Chapel(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.DOMINION
        self.desc = "Trash up to 4 cards"
        self.name = 'Chapel'
        self.cost = 2

    def special(self, game, player):
        """ Trash up to 4 cards from your hand """
        player.plrTrashCard(num=4, prompt="Trash up to four cards")


###############################################################################
class Test_Chapel(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Chapel'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g['Chapel'].remove()
        self.plr.setHand('Copper', 'Silver', 'Estate')
        self.plr.addCard(self.ccard, 'hand')

    def test_trashnone(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['finish']
        self.plr.playCard(self.ccard)
        self.assertEqual(self.plr.handSize(), 3)
        self.assertEqual(self.g.trashSize(), tsize)

    def test_trashtwo(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['trash copper', 'trash silver', 'finish']
        self.plr.playCard(self.ccard)
        self.assertEqual(self.plr.handSize(), 1)
        self.assertEqual(self.g.trashSize(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

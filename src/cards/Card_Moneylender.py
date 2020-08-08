#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Moneylender(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash a copper from hand for +3 coin"
        self.name = 'Money Lender'
        self.cost = 4

    def special(self, game, player):
        """ Trash a copper card from your hand. If you do +3 coin """
        copper = player.in_hand('Copper')
        if not copper:
            player.output("No coppers in hand")
            return
        player.output("Trash a copper to gain +3 coin")
        trash = player.plrChooseOptions(
            "Trash a copper?",
            ("Don't trash a copper", False), ("Trash a copper", True))
        if trash:
            player.trashCard(copper)
            player.addCoin(3)


###############################################################################
class Test_Moneylender(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Money Lender'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Money Lender'].remove()

    def test_nocopper(self):
        tsize = self.g.trashSize()
        self.plr.setHand('Estate', 'Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize)
        self.assertEqual(self.plr.getCoin(), 0)

    def test_trash_copper(self):
        tsize = self.g.trashSize()
        self.plr.test_input = ['1']
        self.plr.setHand('Copper', 'Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.g.in_trash('Copper'))
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertEqual(self.plr.getCoin(), 3)

    def test_dont_trash_copper(self):
        tsize = self.g.trashSize()
        self.plr.setHand('Copper', 'Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashSize(), tsize)
        self.assertEqual(self.plr.getCoin(), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

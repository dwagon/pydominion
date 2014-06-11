#!/usr/bin/env python

import unittest
from Card import Card


class Card_Moneylender(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'dominion'
        self.desc = "Trash a copper from hand for +3 gold"
        self.name = 'Money Lender'
        self.cost = 4

    def special(self, game, player):
        """ Trash a copper card from your hand. If you do +3 Gold """
        copper = player.inHand('copper')
        if not copper:
            player.output("No coppers in hand")
            return
        options = []
        options.append({'selector': '0', 'print': "Don't trash a copper", 'trash': False})
        options.append({'selector': '1', 'print': "Trash a copper", 'trash': True})
        player.output("Trash a copper to gain +3 gold")
        o = player.userInput(options, "Trash a copper?")
        if o['trash']:
            player.trashCard(copper)
            player.t['gold'] += 3


###############################################################################
class Test_Moneylender(unittest.TestCase):
    def setUp(self):
        import Game
        self.g = Game.Game(quiet=True)
        self.g.startGame(numplayers=1, initcards=['moneylender'])
        self.plr = self.g.players.values()[0]
        self.card = self.g['moneylender'].remove()

    def test_nocopper(self):
        self.plr.setHand('estate', 'estate', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashpile, [])
        self.assertEqual(self.plr.t['gold'], 0)

    def test_trash_copper(self):
        self.plr.test_input = ['1']
        self.plr.setHand('copper', 'copper', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashpile[0].name, 'Copper')
        self.assertEqual(len(self.g.trashpile), 1)
        self.assertEqual(self.plr.t['gold'], 3)

    def test_dont_trash_copper(self):
        self.plr.setHand('copper', 'copper', 'estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['0']
        self.plr.playCard(self.card)
        self.assertEqual(self.g.trashpile, [])
        self.assertEqual(self.plr.t['gold'], 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

#EOF

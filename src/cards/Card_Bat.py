#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Bat(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = ['night']
        self.base = Game.NOCTURNE
        self.desc = "Trash up to 2 cards from your hand. If you trashed at least one, exchange this for a Vampire."
        self.name = 'Bat'
        self.cost = 2
        self.insupply = False
        self.purchasable = False

    def night(self, game, player):
        tr = player.plrTrashCard(num=2)
        if tr:
            player.replace_card(self, 'Vampire')


###############################################################################
class Test_Bat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Vampire'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Bat'].remove()

    def test_play(self):
        self.plr.phase = 'night'
        self.plr.setHand('Duchy', 'Silver', 'Gold')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['Trash Silver', 'Trash Gold', 'Finish']
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.in_discard('Bat'))
        self.assertIsNotNone(self.plr.in_discard('Vampire'))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

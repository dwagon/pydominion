#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Spices(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'treasure'
        self.base = Game.RENAISSANCE
        self.name = 'Spices'
        self.coin = 2
        self.buys = 1
        self.cost = 5

    ###########################################################################
    def desc(self, player):
        if player.phase == "buy":
            return "+2 Coin; +1 Buy; When you gain this, +2 Coffers."
        return "+2 Coin; +1 Buy"

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        player.gainCoffer(2)


###############################################################################
class Test_Spices(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Spices'])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_playCard(self):
        self.card = self.g['Spices'].remove()
        self.plr.addCard(self.card, 'hand')
        self.plr.setCoffer(0)
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getBuys(), 1 + 1)
        self.assertEqual(self.plr.getCoin(), 2)
        self.assertEqual(self.plr.getCoffer(), 0)

    def test_gainCard(self):
        self.plr.setCoffer(0)
        self.plr.gainCard('Spices')
        self.assertEqual(self.plr.getBuys(), 1)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.getCoffer(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

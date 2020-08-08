#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Coppersmith(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.INTRIGUE
        self.desc = "Copper produces an extra +1 this turn"
        self.name = 'Coppersmith'
        self.cost = 4

    def hook_spendValue(self, game, player, card):
        """ Copper produces an extra 1 this turn """
        if card.name == 'Copper':
            player.output("Copper worth 1 more")
            return 1
        return 0


###############################################################################
class Test_Coppersmith(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Coppersmith'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Coppersmith'].remove()

    def test_copper(self):
        """ Copper should be worth two """
        self.plr.setHand('Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.playCard(self.plr.hand[0])
        self.assertEqual(self.plr.getCoin(), 2)

    def test_silver(self):
        """ Silver should be unchanged and worth two """
        self.plr.setHand('Silver')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.plr.playCard(self.plr.hand[0])
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

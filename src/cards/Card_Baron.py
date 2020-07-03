#!/usr/bin/env python

import unittest
import Game
from Card import Card


class Card_Baron(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'intrigue'
        self.desc = "+1 Buy. You may discard an Estate card. If you do +4 Coin. Otherwise, gain an Estate card."
        self.name = 'Baron'
        self.cost = 4
        self.buys = 1

    def special(self, game, player):
        """ You may discard an Estate card. If you do +4 Coin. Otherwise,
            gain an estate card """
        hasEstate = player.inHand('Estate')
        if hasEstate:
            ans = player.plrChooseOptions(
                "Discard Estate?",
                ("Keep Estate - Gain another", False),
                ("Discard an Estate - Gain +4 Gold", True)
            )
            if ans:
                player.discardCard(hasEstate)
                player.addCoin(4)
                return
        player.output("Gained an Estate")
        player.gainCard('Estate')


###############################################################################
class Test_Baron(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Baron'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.baron = self.g['Baron'].remove()

    def test_play(self):
        self.plr.addCard(self.baron, 'hand')
        self.plr.test_input = ['Keep']
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.getBuys(), 2)

    def test_noestate(self):
        self.plr.setHand('Copper', 'Copper', 'Copper')
        self.plr.addCard(self.baron, 'hand')
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.discardpile[0].name, 'Estate')
        self.assertEqual(self.plr.discardSize(), 1)

    def test_discardestate(self):
        self.plr.setHand('Gold', 'Estate', 'Copper')
        self.plr.addCard(self.baron, 'hand')
        self.plr.test_input = ['discard']
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.getCoin(), 4)
        self.assertEqual(self.plr.discardpile[0].name, 'Estate')
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertEqual(self.plr.inHand('Estate'), None)

    def test_keepestate(self):
        self.plr.setHand('Estate', 'Gold', 'Copper')
        self.plr.addCard(self.baron, 'hand')
        self.plr.test_input = ['Keep']
        self.plr.playCard(self.baron)
        self.assertEqual(self.plr.getCoin(), 0)
        self.assertEqual(self.plr.discardpile[0].name, 'Estate')
        self.assertEqual(self.plr.discardSize(), 1)
        self.assertNotEqual(self.plr.inHand('Estate'), None)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

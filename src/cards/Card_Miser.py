#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Miser(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = 'action'
        self.base = 'adventure'
        self.desc = "Put a copper onto your mat or +1 coin per copper on mat"
        self.name = 'Miser'
        self.cost = 4

    def special(self, game, player):
        """ Choose one: Put a Copper from your hand onto your Tavern mat;
        or +1 Coin per Copper on your Tavern mat."""
        inhand = sum([1 for c in player.hand if c.name == 'Copper'])
        coins = sum([1 for c in player.reserve if c.name == 'Copper'])
        deposit = False
        if inhand:
            deposit = player.plrChooseOptions(
                "Which to do?",
                ("Put a copper onto tavern mat?", True),
                ("%d coins from mat" % coins, False))
            if deposit:
                cu = player.inHand('Copper')
                player.addCard(cu, 'reserve')
                player.hand.remove(cu)
        if not deposit:
            player.output("Adding %d coins from tavern" % coins)
            player.addCoin(coins)


###############################################################################
class Test_Miser(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Miser'])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g['Miser'].remove()

    def test_put(self):
        """ Play a miser with coppers in hand"""
        self.plr.setHand('Copper', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['put']
        self.plr.playCard(self.card)
        self.assertIsNotNone(self.plr.inReserve('Copper'))
        self.assertEqual(self.plr.reserveSize(), 1)
        self.assertIsNone(self.plr.inHand('Copper'))

    def test_put_none(self):
        """ Play a miser with no coppers in hand"""
        self.plr.setHand('Estate', 'Estate')
        self.plr.addCard(self.card, 'hand')
        self.plr.playCard(self.card)
        self.assertIsNone(self.plr.inReserve('Copper'))
        self.assertEqual(self.plr.reserveSize(), 0)

    def test_add(self):
        """ Play a miser with coppers in reserve """
        self.plr.setHand('Copper', 'Estate')
        self.plr.setReserve('Copper', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['coins from mat']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.reserveSize(), 2)
        self.assertEqual(self.plr.getCoin(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

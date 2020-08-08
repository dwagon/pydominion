#!/usr/bin/env python

import unittest
import Game
from Card import Card


###############################################################################
class Card_Forum(Card):
    def __init__(self):
        Card.__init__(self)
        self.cardtype = Card.ACTION
        self.base = Game.EMPIRES
        self.name = 'Forum'
        self.cards = 3
        self.actions = 1
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return "+3 Cards, +1 Action, Discard 2 cards. When you buy this, +1 Buy."
        return "+3 Cards, +1 Action, Discard 2 cards."

    def special(self, game, player):
        player.plrDiscardCards(num=2, force=True)

    def hook_buy_this_card(self, game, player):
        player.addBuys(1)


###############################################################################
class Test_Forum(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=['Forum'])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g['Forum'].remove()

    def test_play(self):
        """ Play a Forum """
        self.plr.setHand('Gold', 'Duchy', 'Estate', 'Province', 'Copper')
        self.plr.addCard(self.card, 'hand')
        self.plr.test_input = ['duchy', 'province', 'finish']
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.handSize(), 5 + 3 - 2)

    def test_buy(self):
        self.plr.setCoin(5)
        self.plr.buyCard(self.g['Forum'])
        self.assertEqual(self.plr.getBuys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

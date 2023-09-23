#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Port(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Port"
        self.cards = 1
        self.actions = 2
        self.cost = 4
        self.numcards = 12

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return "+1 Card, +2 Actions; When you buy this, gain another Port"
        return "+1 Card, +2 Actions"

    def hook_buy_this_card(self, game, player):
        """Gain another Port"""
        c = player.gain_card("Port")
        if c:
            player.output("Gained a port")
        else:
            player.output("No more ports")


###############################################################################
class TestPort(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Port"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Port")

    def test_play(self):
        """Play a port"""
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_buy(self):
        """Buy a port"""
        self.plr.piles[Piles.DISCARD].set()
        self.plr.coins.set(5)
        self.plr.buy_card("Port")
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Port")
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

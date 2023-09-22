#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Lost_City(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.name = "Lost City"
        self.cards = 2
        self.actions = 2
        self.cost = 5

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return "+2 Cards, +2 Actions; When you gain this every else gains a card"
        return "+2 Cards, +2 Actions"

    def special(self, game, player):
        pass

    def hook_gain_this_card(self, game, player):
        """When you gain this, each other player draws a card"""
        for pl in game.player_list():
            if pl != player:
                c = pl.pickup_card()
                pl.output(
                    "Picking up a %s due to %s playing a Lost City"
                    % (c.name, player.name)
                )
        return {}


###############################################################################
class TestLostCity(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Lost City"])
        self.g.start_game()
        self.plr, self.other = self.g.player_list()
        self.card = self.g.get_card_from_pile("Lost City")

    def test_play(self):
        """Play a lost_city"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 2)
        self.assertTrue(self.other.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

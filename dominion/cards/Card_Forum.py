#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Forum(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.name = "Forum"
        self.cards = 3
        self.actions = 1
        self.cost = 5

    def desc(self, player):
        if player.phase == "buy":
            return "+3 Cards, +1 Action, Discard 2 cards. When you buy this, +1 Buy."
        return "+3 Cards, +1 Action, Discard 2 cards."

    def special(self, game, player):
        player.plr_discard_cards(num=2, force=True)

    def hook_buy_this_card(self, game, player):
        player.add_buys(1)


###############################################################################
class Test_Forum(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Forum"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Forum"].remove()

    def test_play(self):
        """Play a Forum"""
        self.plr.hand.set("Gold", "Duchy", "Estate", "Province", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["duchy", "province", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 5 + 3 - 2)

    def test_buy(self):
        self.plr.coins.set(5)
        self.plr.buy_card(self.g["Forum"])
        self.assertEqual(self.plr.get_buys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

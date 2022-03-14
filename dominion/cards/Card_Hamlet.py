#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Hamlet(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.CORNUCOPIA
        self.desc = "+1 Card +1 Action. You may discard a card; if you do, +1 Action.  You may discard a card; if you do, +1 Buy."
        self.name = "Hamlet"
        self.cards = 1
        self.actions = 1
        self.cost = 2

    def special(self, game, player):
        c = player.plrDiscardCards(prompt="Discard a card to gain an action")
        if c:
            player.add_actions(1)
        c = player.plrDiscardCards(prompt="Discard card to gain a buy")
        if c:
            player.add_buys(1)


###############################################################################
class Test_Hamlet(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Hamlet"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hamlet"].remove()
        self.plr.set_hand("Silver", "Gold")
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a hamlet"""
        self.plr.test_input = ["finish selecting", "finish selecting"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 3)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_discard_action(self):
        """Play a hamlet and discard to gain an action"""
        self.plr.test_input = ["discard silver", "finish selecting"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertIsNone(self.plr.in_hand("Silver"))

    def test_discard_buy(self):
        """Play a hamlet and discard to gain a buy"""
        self.plr.test_input = ["finish selecting", "discard gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertIsNone(self.plr.in_hand("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

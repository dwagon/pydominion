#!/usr/bin/env python

import unittest
from dominion import Game, Card


###############################################################################
class Card_Town(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ALLIES
        self.name = "Town"
        self.desc = """Choose one: +1 Card and +2 Actions; or +1 Buy and +$2."""
        self.cost = 4

    def special(self, game, player):
        choice = player.plr_choose_options(
            "Choose One:",
            ("+1 Card and +2 Actions", "card"),
            ("+1 Buy and +$2 Coin", "buy"),
        )
        if choice == "card":
            player.pickup_cards(1)
            player.add_actions(2)
        elif choice == "buy":
            player.add_buys(1)
            player.add_coins(2)


###############################################################################
class Test_Town(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Town"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Town"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_card_actions(self):
        """Play the card and card + actions"""
        self.plr.test_input = ["card"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 1)
        self.assertEqual(self.plr.get_actions(), 1 + 1)

    def test_play_buy_cash(self):
        """Play the card and buy + coin"""
        self.plr.test_input = ["buy"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.get_buys(), 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

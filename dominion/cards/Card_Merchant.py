#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Merchant(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DOMINION
        self.desc = (
            "+1 Card; +1 Action; The first time you play a Silver this turn, +1 Coin."
        )
        self.name = "Merchant"
        self.actions = 1
        self.cards = 1
        self.cost = 3

    def hook_spend_value(self, game, player, card):
        if card.name != "Silver":
            return 0
        ag_count = player.played.count("Silver")
        if ag_count == 1:
            return 1
        return 0


###############################################################################
class Test_Merchant(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Merchant"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Merchant"].remove()
        self.s1 = self.g["Silver"].remove()
        self.s2 = self.g["Silver"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 6)
        self.plr.add_card(self.s1, "hand")
        self.plr.play_card(self.s1)
        self.assertEqual(self.plr.get_coins(), 3)
        self.plr.add_card(self.s2, "hand")
        self.plr.play_card(self.s2)
        self.assertEqual(self.plr.get_coins(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

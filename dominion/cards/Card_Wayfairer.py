#!/usr/bin/env python
""" http://wiki.dominionstrategy.com/index.php/Wayfarer """

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Wayfarer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.MENAGERIE
        self.desc = "+3 Cards; You may gain a Silver. This has the same cost as the last other card gained this turn, if any."
        self.name = "Wayfarer"
        self.cards = 3
        self.cost = 6

    def special(self, game, player):
        player.gainCard("Silver")
        player.output("Gained a Silver")

    def hook_this_card_cost(self, game, player):
        if player.stats["gained"]:
            last_cost = player.stats["gained"][0].cost
            delta = -6 + last_cost
            return delta
        return 0


###############################################################################
class Test_Wayfarer(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Wayfarer"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Wayfarer"].remove()
        self.plr.add_card(self.card, "hand")

    def test_playcard(self):
        """Play a wayfairer"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 5 + 3)
        self.assertIsNotNone(self.plr.in_discard("Silver"))

    def test_buy(self):
        """Buy a wayfairer"""
        cost = self.plr.cardCost(self.card)
        self.assertEqual(cost, 6)
        self.plr.gainCard("Estate")
        cost = self.plr.cardCost(self.card)
        self.assertEqual(cost, 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

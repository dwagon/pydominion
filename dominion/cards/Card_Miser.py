#!/usr/bin/env python

import unittest
from dominion import Card, Game


###############################################################################
class Card_Miser(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.ADVENTURE
        self.desc = "Put a copper onto your mat or +1 coin per copper on mat"
        self.name = "Miser"
        self.cost = 4

    def special(self, game, player):
        """Choose one: Put a Copper from your hand onto your Tavern mat;
        or +1 Coin per Copper on your Tavern mat."""
        inhand = sum([1 for _ in player.hand if _.name == "Copper"])
        coins = sum([1 for _ in player.reserve if _.name == "Copper"])
        deposit = False
        if inhand:
            deposit = player.plr_choose_options(
                "Which to do?",
                ("Put a copper onto tavern mat?", True),
                ("%d coins from mat" % coins, False),
            )
            if deposit:
                cu = player.in_hand("Copper")
                player.add_card(cu, Card.TYPE_RESERVE)
                player.hand.remove(cu)
        if not deposit:
            player.output("Adding %d coins from tavern" % coins)
            player.add_coins(coins)


###############################################################################
class Test_Miser(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Miser"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Miser"].remove()

    def test_put(self):
        """Play a miser with coppers in hand"""
        self.plr.set_hand("Copper", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["put"]
        self.plr.play_card(self.card)
        self.assertIsNotNone(self.plr.in_reserve("Copper"))
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertIsNone(self.plr.in_hand("Copper"))

    def test_put_none(self):
        """Play a miser with no coppers in hand"""
        self.plr.set_hand("Estate", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIsNone(self.plr.in_reserve("Copper"))
        self.assertEqual(self.plr.reserve.size(), 0)

    def test_add(self):
        """Play a miser with coppers in reserve"""
        self.plr.set_hand("Copper", "Estate")
        self.plr.set_reserve("Copper", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["coins from mat"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.reserve.size(), 2)
        self.assertEqual(self.plr.get_coins(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

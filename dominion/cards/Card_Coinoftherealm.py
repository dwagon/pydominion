#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Coinoftherealm(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = "+1 Coin; Call for +2 Actions"
        self.name = "Coin of the Realm"
        self.coin = 1
        self.cost = 2
        self.when = "postaction"

    def hook_call_reserve(self, game, player):
        """Directly after resolving an action you may call this for +2 Actions"""
        player.add_actions(2)


###############################################################################
class Test_Coinoftherealm(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Coin of the Realm"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Coin of the Realm"].remove()

    def test_play(self):
        """Play a coin of the realm"""
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertIn("Coin of the Realm", self.plr.reserve)

    def test_call(self):
        """Call from Reserve"""
        self.plr.actions = 0
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        c = self.plr.call_reserve("Coin of the Realm")
        self.assertEqual(c.name, "Coin of the Realm")
        self.assertEqual(self.plr.get_actions(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

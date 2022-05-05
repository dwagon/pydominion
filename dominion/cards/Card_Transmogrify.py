#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Transmogrify(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = """+1 Action; At the start of your turn, you may call this,
            to trash a card from your hand, gain a card costing up to 1 coin more
            than it, and put that card into your hand"""
        self.name = "Transmogrify"
        self.actions = 1
        self.when = "start"
        self.cost = 4

    def hook_call_reserve(self, game, player):
        tc = player.plr_trash_card(
            printcost=True,
            prompt="Trash a card from you hand. Gain a card costing up to 1 more",
        )
        if tc:
            cost = player.card_cost(tc[0])
            player.plr_gain_card(cost + 1, modifier="less", destination="hand")


###############################################################################
class Test_Transmogrify(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Transmogrify"],
            badcards=["Duchess", "Fool's Gold"],
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.trans = self.g["Transmogrify"].remove()
        self.plr.add_card(self.trans, "hand")

    def test_play(self):
        self.plr.play_card(self.trans)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertIsNotNone(self.plr.reserve["Transmogrify"])

    def test_call(self):
        self.plr.set_hand("Duchy", "Estate")
        self.plr.set_reserve("Transmogrify")
        self.plr.test_input = ["trash duchy", "get gold"]
        self.plr.call_reserve("Transmogrify")
        self.assertIsNotNone(self.g.in_trash("Duchy"))
        self.assertIn("Gold", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

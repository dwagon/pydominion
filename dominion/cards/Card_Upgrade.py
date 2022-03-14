#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Upgrade(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.INTRIGUE
        self.desc = "+1 Card, +1 Action. Trash a card from your hand. Gain a card costing exactly 1 more than it."
        self.name = "Upgrade"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def special(self, game, player):
        """Trash a card from your hand. Gain a card costing up to 1 more than it"""
        tc = player.plrTrashCard(
            printcost=True,
            prompt="Trash a card from your hand. Gain a card costing exactly 1 more than it",
        )
        if tc:
            cost = player.card_cost(tc[0])
            player.plrGainCard(cost + 1, "equal")


###############################################################################
class Test_Upgrade(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Upgrade"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Upgrade"].remove()

    def test_play(self):
        """Play the Upgrade"""
        tsize = self.g.trashSize()
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["0"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.g.trashSize(), tsize)

    def test_trash(self):
        """Trash an upgrade"""
        tsize = self.g.trashSize()
        self.plr.set_hand("Duchy", "Copper")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Duchy", "Get Gold"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 2)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Duchy"))
        self.assertEqual(self.plr.discardpile.size(), 1)
        self.assertIsNotNone(self.plr.in_discard("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Ratcatcher(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RESERVE]
        self.base = Game.ADVENTURE
        self.desc = "+1 Card, +1 Action; Call to trash a card"
        self.name = "Ratcatcher"
        self.cards = 1
        self.actions = 1
        self.cost = 2
        self.when = "start"

    def hook_call_reserve(self, game, player):
        """At the start of your turn, you may call this, to trash a
        card from your hand"""
        player.plrTrashCard()


###############################################################################
class Test_Ratcatcher(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Ratcatcher"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Ratcatcher"].remove()

    def test_play(self):
        """Play a ratcatcher"""
        self.plr.setHand()
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.reserve.size(), 1)
        c = self.plr.in_reserve("Ratcatcher")
        self.assertEqual(c.name, "Ratcatcher")

    def test_call(self):
        """Call from Reserve"""
        tsize = self.g.trashSize()
        self.plr.setHand("Gold")
        self.plr.addCard(self.card, "hand")
        self.plr.test_input = ["Trash Gold"]
        self.plr.playCard(self.card)
        c = self.plr.call_reserve("Ratcatcher")
        self.assertEqual(c.name, "Ratcatcher")
        self.assertEqual(self.g.trashSize(), tsize + 1)
        self.assertIsNotNone(self.g.in_trash("Gold"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

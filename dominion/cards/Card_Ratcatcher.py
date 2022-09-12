#!/usr/bin/env python

import unittest
from dominion import Card, Game


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
        player.plr_trash_card()


###############################################################################
class Test_Ratcatcher(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Ratcatcher"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Ratcatcher"].remove()

    def test_play(self):
        """Play a ratcatcher"""
        self.plr.hand.set()
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.hand.size(), 1)
        self.assertEqual(self.plr.reserve.size(), 1)
        self.assertIn("Ratcatcher", self.plr.reserve)

    def test_call(self):
        """Call from Reserve"""
        tsize = self.g.trashpile.size()
        self.plr.hand.set("Gold")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Trash Gold"]
        self.plr.play_card(self.card)
        c = self.plr.call_reserve("Ratcatcher")
        self.assertEqual(c.name, "Ratcatcher")
        self.assertEqual(self.g.trashpile.size(), tsize + 1)
        self.assertIn("Gold", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

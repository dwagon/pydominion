#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Tactician(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.SEASIDE
        self.desc = "Discard hand; +5 cards, +1 buy and +1 action next turn"
        self.name = "Tactician"
        self.cost = 5

    def special(self, game, player):
        self.discarded = False
        discard = player.plrChooseOptions(
            "Discard hand for good stuff next turn?", ("Keep", False), ("Discard", True)
        )
        if discard and player.hand.size():
            self.discarded = True
            player.discard_hand()

    def duration(self, game, player):
        """+5 Cards, +1 Buy, +1 Action"""
        if self.discarded:
            player.pickup_cards(5)
            player.add_buys(1)
            player.addActions(1)
            self.discarded = False


###############################################################################
class Test_Tactician(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Tactician"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Tactician"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_discard(self):
        """Play a tactician and discard hand"""
        self.plr.test_input = ["discard"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 0)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 10)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.get_buys(), 2)

    def test_play_keep(self):
        """Play a tactician and discard hand"""
        self.plr.test_input = ["keep"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 5)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 5)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.get_buys(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

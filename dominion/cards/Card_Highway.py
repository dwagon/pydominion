#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Highway(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.desc = (
            "+1 Card +1 Action. While this is in play, cards cost 1 less, but not less than 0."
        )
        self.name = "Highway"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def hook_card_cost(self, game, player, card):
        if self in player.played:
            return -1
        return 0


###############################################################################
class Test_Highway(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Highway"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Highway"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertEqual(self.plr.get_actions(), 1)

    def test_costreduction(self):
        self.coin = 1
        self.assertEqual(self.plr.card_cost(self.g["Gold"]), 6)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.card_cost(self.g["Gold"]), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

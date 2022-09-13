#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bordervillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.HINTERLANDS
        self.name = "Border Village"
        self.cost = 6
        self.cards = 1
        self.actions = 2

    def desc(self, player):
        if player.phase == "buy":
            return "+1 card, +2 action. When you gain this, gain a card costing less than this"
        return "+1 card, +2 action"

    def hook_gain_this_card(self, game, player):
        """When you gain this, gain a card costing less than this"""
        newcost = self.cost - 1
        player.plr_gain_card(
            cost=newcost,
            prompt="Gain a card costing %d due to Border Village" % newcost,
        )
        return {}


###############################################################################
class Test_Bordervillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Border Village"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.bv = self.g["Border Village"].remove()
        self.plr.add_card(self.bv, "hand")

    def test_play(self):
        self.plr.play_card(self.bv)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.hand.size(), 6)

    def test_gain(self):
        self.plr.test_input = ["get estate"]
        self.plr.gain_card("Border Village")
        self.assertEqual(self.plr.discardpile.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

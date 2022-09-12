#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Villa(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.EMPIRES
        self.name = "Villa"
        self.cost = 4
        self.actions = 2
        self.buys = 1
        self.coin = 1

    def desc(self, player):
        if player.phase == Card.TYPE_ACTION:
            return "+2 Actions; +1 Buy; +1 Coin"
        return """+2 Actions; +1 Buy; +1 Coin; When you gain this, put it into
            your hand, +1 Action, and if it's your Buy phase return to your
            Action phase."""

    def hook_gain_this_card(self, game, player):
        if player.phase == "buy":
            player.phase = Card.TYPE_ACTION
        player.add_actions(1)
        return {"destination": "hand"}


###############################################################################
class Test_Villa(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Villa"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Villa"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 2)

    def test_gain(self):
        self.plr.phase = "buy"
        self.plr.gain_card("Villa")
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.phase, Card.TYPE_ACTION)
        self.assertIn("Villa", self.plr.hand)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

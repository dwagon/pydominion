#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Mill(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_VICTORY]
        self.base = Game.INTRIGUE
        self.name = "Mill"
        self.desc = "+1 Card; +1 Action; You may discard 2 cards, for +2 Coin; 1VP"
        self.cost = 4
        self.actions = 1
        self.victory = 1
        self.cards = 1

    def special(self, game, player):
        dc = player.plr_discard_cards(num=2)
        if len(dc) == 2:
            player.coins.add(2)


###############################################################################
class Test_Mill(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Mill"], badcards=["Duchess"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Mill"].remove()

    def test_play(self):
        self.plr.hand.set("Gold", "Silver")
        self.plr.test_input = ["Discard Gold", "Finish"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.hand.size(), 1 + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.get_score_details()["Mill"], 1)
        self.assertIn("Gold", self.plr.discardpile)

    def test_discard(self):
        self.plr.hand.set("Gold", "Silver")
        self.plr.test_input = ["Discard Gold", "Discard Silver", "Finish"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertIn("Silver", self.plr.discardpile)
        self.assertEqual(self.plr.coins.get(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Overgrown_Estate(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_VICTORY, Card.TYPE_SHELTER]
        self.base = Game.DARKAGES
        self.desc = "0VP; When you trash this, +1 Card."
        self.name = "Overgrown Estate"
        self.cost = 1
        self.purchasable = False

    def hook_trashThisCard(self, game, player):
        player.pickup_card()


###############################################################################
class Test_Overgrown_Estate(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Overgrown Estate"].remove()

    def test_play(self):
        self.plr.hand.set("Province", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertIsNotNone(self.g.in_trash("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Cemetery(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.NOCTURNE
        self.desc = "+2 VP; When you gain this, trash up to 4 cards from your hand."
        self.name = "Cemetery"
        self.cost = 4
        self.victory = 2
        self.heirloom = "Haunted Mirror"

    def hook_gain_this_card(self, game, player):
        player.plr_trash_card(num=4)


###############################################################################
class Test_Cemetery(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Cemetery"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cemetery"].remove()

    def test_gain(self):
        """Gain a Cemetery"""
        self.plr.hand.set("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.test_input = ["Copper", "Silver", "Gold", "Estate", "Finish"]
        self.plr.gain_card("Cemetery")
        self.assertIn("Copper", self.g.trashpile)
        self.assertIn("Gold", self.g.trashpile)
        self.assertNotIn("Duchy", self.g.trashpile)
        self.assertEqual(self.plr.get_score_details()["Cemetery"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

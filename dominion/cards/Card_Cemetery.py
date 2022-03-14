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
        player.plrTrashCard(num=4)


###############################################################################
class Test_Cemetery(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Cemetery"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Cemetery"].remove()

    def test_gain(self):
        """Gain a Cemetery"""
        self.plr.set_hand("Copper", "Silver", "Gold", "Estate", "Duchy", "Province")
        self.plr.test_input = ["Copper", "Silver", "Gold", "Estate", "Finish"]
        self.plr.gainCard("Cemetery")
        self.assertIsNotNone(self.g.in_trash("Copper"))
        self.assertIsNotNone(self.g.in_trash("Gold"))
        self.assertIsNone(self.g.in_trash("Duchy"))
        self.assertEqual(self.plr.get_score_details()["Cemetery"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

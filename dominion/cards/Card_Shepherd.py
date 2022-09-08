#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Shepherd(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.NOCTURNE
        self.desc = "+1 action; Discard any number of victory cards +2 cards per card discarded"
        self.name = "Shepherd"
        self.cost = 2
        self.actions = 1
        self.heirloom = "Pasture"

    def special(self, game, player):
        todiscard = player.plr_discard_cards(num=0, anynum=True, types={Card.TYPE_VICTORY: True})
        player.pickup_cards(2 * len(todiscard))


###############################################################################
class Test_Shepherd(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Shepherd"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Shepherd"].remove()

    def test_play(self):
        """Play a Shepherd"""
        self.plr.hand.set("Estate", "Province", "Duchy")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 1)
        self.assertEqual(self.plr.hand.size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

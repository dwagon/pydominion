#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Madman(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.DARKAGES
        self.desc = """+2 Actions. Return this to the Madman pile. If you do, +1 Card per card in your hand."""
        self.name = "Madman"
        self.insupply = False
        self.actions = 2
        self.cost = 0
        self.purchasable = False

    def special(self, game, player):
        handsize = player.hand.size()
        player.output("Gaining %d cards from madman" % handsize)
        for _ in range(handsize):
            player.pickup_card()
        game["Madman"].add(self)
        player.played.remove(self)


###############################################################################
class Test_Madman(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hermit"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Madman"].remove()

    def test_play(self):
        """Play a Madman"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_actions(), 2)
        self.assertEqual(self.plr.hand.size(), 5 * 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

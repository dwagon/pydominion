#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Hireling(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_DURATION]
        self.base = Game.ADVENTURE
        self.desc = "+1 Card forever"
        self.name = "Hireling"
        self.cost = 6
        self.permanent = True

    def special(self, game, player):
        pass

    def duration(self, game, player):
        player.pickup_card()


###############################################################################
class Test_Hireling(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Hireling"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hireling"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play_hireling(self):
        """Play a hireling"""
        self.plr.play_card(self.card)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.hand.size(), 6)
        self.assertNotIn("Hireling", self.plr.discardpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

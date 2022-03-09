#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Scholar(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_ACTION
        self.base = Game.RENAISSANCE
        self.desc = """Discard your hand. +7 Cards."""
        self.name = "Scholar"
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        player.discardHand()
        player.pickupCards(7)


###############################################################################
class Test_Scholar(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Scholar"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Scholar"].remove()

    def test_play(self):
        self.plr.addCard(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.hand.size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

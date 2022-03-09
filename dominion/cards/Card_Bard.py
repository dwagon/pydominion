#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Bard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_FATE]
        self.base = Game.NOCTURNE
        self.desc = "+2 Coin; Receive a boon"
        self.name = "Bard"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        player.receive_boon()


###############################################################################
class Test_Bard(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.bard = self.g["Bard"].remove()
        for b in self.g.boons[:]:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break

    def test_play_card(self):
        """Play Bard"""
        self.plr.addCard(self.bard, "hand")
        self.plr.playCard(self.bard)
        self.assertGreaterEqual(self.plr.getCoin(), 2)
        # Check boon happened
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

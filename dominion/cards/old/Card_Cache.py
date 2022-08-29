#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Cache(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.HINTERLANDS
        self.name = "Cache"
        self.cost = 5
        self.coin = 3

    def desc(self, player):
        if player.phase == "buy":
            return "+3 coin. Gain two coppers when you gain this"
        return "+3 coin"

    def hook_gain_this_card(self, game, player):
        """When you gain this, gain two Coppers"""
        player.output("Gained 2 copper from cache")
        for _ in range(2):
            player.gain_card("Copper")
        return {}


###############################################################################
class Test_Cache(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, oldcards=True, initcards=["Cache"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.cache = self.g["Cache"].remove()

    def test_gain(self):
        self.plr.gain_card("Cache")
        sdp = sorted([c.name for c in self.plr.discardpile])
        self.assertEqual(sorted(["Copper", "Copper", "Cache"]), sdp)

    def test_play(self):
        self.plr.add_card(self.cache, "hand")
        self.plr.play_card(self.cache)
        self.assertEqual(self.plr.get_coins(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
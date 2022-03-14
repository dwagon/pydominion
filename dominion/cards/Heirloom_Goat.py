#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Goat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_HEIRLOOM]
        self.base = Game.NOCTURNE
        self.desc = "When you play this, you may trash a card from your hand."
        self.name = "Goat"
        self.cost = 2
        self.coin = 1
        self.purchasable = False

    def special(self, game, player):
        if player.hand.size():
            player.plr_trash_card()


###############################################################################
def botresponse(player, kind, args=None, kwargs=None):  # pragma: no cover
    return []


###############################################################################
class Test_Goat(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Pixie"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Goat"].remove()

    def test_play(self):
        self.plr.set_hand("Province", "Estate")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Province"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_coins(), 1)
        self.assertIsNotNone(self.g.in_trash("Province"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

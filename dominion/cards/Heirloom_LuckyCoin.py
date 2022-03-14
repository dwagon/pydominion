#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_LuckyCoin(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_HEIRLOOM]
        self.base = Game.NOCTURNE
        self.desc = "1 Coin; When you play this, gain a Silver."
        self.name = "Lucky Coin"
        self.cost = 4
        self.coin = 1
        self.purchasable = False

    def special(self, game, player):
        player.gain_card("Silver")


###############################################################################
class Test_LuckyCoin(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Fool"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Lucky Coin"].remove()

    def test_play(self):
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.getCoin(), 1)
        self.assertEqual(self.plr.discardpile[0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Spices(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_TREASURE
        self.base = Game.RENAISSANCE
        self.name = "Spices"
        self.coin = 2
        self.buys = 1
        self.cost = 5

    ###########################################################################
    def desc(self, player):
        if player.phase == "buy":
            return "+2 Coin; +1 Buy; When you gain this, +2 Coffers."
        return "+2 Coin; +1 Buy"

    ###########################################################################
    def hook_gain_this_card(self, game, player):
        player.add_coffer(2)


###############################################################################
class Test_Spices(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Spices"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play_card(self):
        self.card = self.g["Spices"].remove()
        self.plr.add_card(self.card, "hand")
        self.plr.set_coffers(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 1 + 1)
        self.assertEqual(self.plr.get_coins(), 2)
        self.assertEqual(self.plr.get_coffers(), 0)

    def test_gain_card(self):
        self.plr.set_coffers(0)
        self.plr.gain_card("Spices")
        self.assertEqual(self.plr.get_buys(), 1)
        self.assertEqual(self.plr.get_coins(), 0)
        self.assertEqual(self.plr.get_coffers(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

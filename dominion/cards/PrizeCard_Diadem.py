#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Diadem(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_TREASURE, Card.TYPE_PRIZE]
        self.base = Game.CORNUCOPIA
        self.name = "Diadem"
        self.purchasable = False
        self.cost = 0
        self.desc = "2 Coin. When you play this, +1 Coin per unused Action you have (Action, not Action card)."
        self.coin = 2

    def special(self, game, player):
        player.output("Gaining %d coins from unused actions" % player.actions)
        player.add_coins(player.actions)


###############################################################################
class Test_Diadem(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Tournament"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Diadem"].remove()
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        self.plr.play_card(self.card)
        self.plr.actions = 1
        self.assertEqual(self.plr.get_coins(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Hero(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_TRAVELLER]
        self.base = Game.ADVENTURE
        self.desc = "+2 Coin, Gain a Treasure; Discard to replace with Champion"
        self.name = "Hero"
        self.purchasable = False
        self.coin = 2
        self.cost = 5
        self.numcards = 5

    def special(self, game, player):
        """Gain a treasure"""
        player.plr_gain_card(cost=None, types={Card.TYPE_TREASURE: True})

    def hook_discard_this_card(self, game, player, source):
        """Replace with Champion"""
        player.replace_traveller(self, "Champion")


###############################################################################
class Test_Hero(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(
            quiet=True, numplayers=1, initcards=["Page"], badcards=["Fool's Gold"]
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Hero"].remove()
        self.plr.add_card(self.card, "hand")

    def test_hero(self):
        """Play a hero"""
        self.plr.test_input = ["get gold"]
        self.plr.play_card(self.card)
        try:
            self.assertEqual(self.plr.get_coins(), 2)
            self.assertIsNotNone(self.plr.in_discard("Gold"))
        except AssertionError:  # pragma: no cover
            self.g.print_state()
            raise


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Horsetraders(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_REACTION]
        self.base = Game.CORNUCOPIA
        self.desc = """+1 Buy. +3 Coins. Discard 2 cards.
        When another player plays an Attack card, you may set this aside from your hand.
        If you do, then at the start of your next turn, +1 Card and return this to your hand."""
        self.name = "Horse Traders"
        self.buys = 1
        self.coin = 3
        self.cost = 4

    def special(self, game, player):
        player.plr_discard_cards(num=2)

    def todo(self):  # TODO
        """When another player plays an Attack card, you may set
        this aside from your hand.  If you do, then at the start
        of your next turn, +1 Card and return this to your hand."""


###############################################################################
class Test_Horsetraders(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Horse Traders"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Horse Traders"].remove()

    def test_play(self):
        self.plr.hand.set("Estate", "Duchy", "Province")
        self.plr.add_card(self.card, "hand")
        self.plr.test_input = ["Estate", "Duchy", "Finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_buys(), 2)
        self.assertEqual(self.plr.get_coins(), 3)
        self.assertEqual(self.plr.discardpile.size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

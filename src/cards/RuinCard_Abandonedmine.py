#!/usr/bin/env python

import unittest
import Game
import Card


###############################################################################
class Card_AbandonedMine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_RUIN]
        self.base = Game.DARKAGES
        self.name = "Abandoned Mine"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 coin"
        self.coin = 1


###############################################################################
class Test_AbandonedMine(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Ruins"].remove()
            if self.card.name == "Abandoned Mine":
                break
        self.plr.addCard(self.card, "hand")

    def test_play(self):
        """Play an abandoned mine"""
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.getCoin(), 1)


# EOF

#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_AbandonedMine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Abandoned Mine"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 coin"
        self.coin = 1


###############################################################################
class Test_AbandonedMine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Ruins"].remove()
            if self.card.name == "Abandoned Mine":
                break
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play an abandoned mine"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)


# EOF

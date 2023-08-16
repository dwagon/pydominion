#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_RuinedMarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Ruined Market"
        self.desc = "+1 Buy"
        self.purchasable = False
        self.cost = 0
        self.buys = 1


###############################################################################
class Test_RuinedMarket(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Ruins"].remove()
            if self.card.name == "Ruined Market":
                break
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a ruined market"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1 + 1)


# EOF

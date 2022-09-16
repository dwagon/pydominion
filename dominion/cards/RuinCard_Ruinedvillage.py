#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_RuinedVillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Ruined Village"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 Action"
        self.actions = 1


###############################################################################
class Test_RuinedVillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Ruins"].remove()
            if self.card.name == "Ruined Village":
                break
        self.plr.add_card(self.card, "hand")

    def test_play(self):
        """Play a ruined village"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)


# EOF

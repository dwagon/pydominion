#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_CrumblingCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.CASTLE]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 4
        self.desc = "1VP. When you gain or trash this, +1VP and gain a Silver."
        self.victory = 1
        self.name = "Crumbling Castle"
        self.pile = "Castles"

    def hook_gain_this_card(self, game, player):
        player.add_score("Crumbling Castle", 1)
        player.gain_card("Silver")

    def hook_trash_this_card(self, game, player):
        player.add_score("Crumbling Castle", 1)
        player.gain_card("Silver")


###############################################################################
class TestCrumblingCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Castles", "Crumbling Castle")

    def test_play(self):
        """Play a castle"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Crumbling Castle"], 1)

    def test_trash(self):
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Crumbling Castle"], 1)
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

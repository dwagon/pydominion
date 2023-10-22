#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fairgrounds(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.CORNUCOPIA
        self.desc = "2VP / 5 card types"
        self.name = "Fairgrounds"
        self.playable = False
        self.cost = 6

    def special_score(self, game, player):
        """Worth 2VP for every 5 differently named cards in your deck (round down)"""
        numtypes = {c.name for c in player.all_cards()}
        return 2 * int(len(numtypes) / 5)


###############################################################################
class Test_Fairgrounds(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Fairgrounds"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fairgrounds")

    def test_zero(self):
        """Fairground for 4 types"""
        self.plr.piles[Piles.HAND].set("Copper", "Estate", "Silver", "Fairgrounds")
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Silver", "Fairgrounds")
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Fairgrounds"], 0)

    def test_one(self):
        """Fairground for 4 types"""
        self.plr.piles[Piles.DECK].set("Copper", "Estate", "Silver", "Fairgrounds", "Gold")
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Fairgrounds"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

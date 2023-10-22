#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Pasture(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.TREASURE,
            Card.CardType.VICTORY,
            Card.CardType.HEIRLOOM,
        ]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Coin; Worth 1VP per Estate you have"
        self.name = "Pasture"
        self.cost = 2
        self.coin = 1
        self.purchasable = False

    def special_score(self, game, player):
        estates = sum([1 for _ in player.all_cards() if _.name == "Estate"])
        return estates


###############################################################################
class Test_Pasture(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Shepherd"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pasture")

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_score(self):
        self.plr.piles[Piles.HAND].set("Estate", "Pasture")
        self.plr.piles[Piles.DECK].set("Estate")
        score = self.plr.get_score_details()
        self.assertEqual(score["Pasture"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

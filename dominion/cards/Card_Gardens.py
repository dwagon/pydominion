#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Gardens(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Worth 1VP per 10 cards you have (round down)."
        self.name = "Gardens"
        self.playable = False
        self.cost = 4

    def special_score(self, game, player):
        """Worth 1VP for every 10 cards in your deck rounded down"""
        numcards = len(player.all_cards())
        return int(numcards / 10)


###############################################################################
class Test_Gardens(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Gardens"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_score_0(self):
        self.plr.piles[Piles.HAND].set("Gardens", "Copper", "Copper")
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper")
        self.plr.piles[Piles.DISCARD].set("Copper", "Copper", "Copper")
        score = self.plr.get_score_details()
        self.assertEqual(score["Gardens"], 0)

    def test_score_1(self):
        self.plr.piles[Piles.HAND].set("Gardens", "Copper", "Copper")
        self.plr.piles[Piles.DECK].set("Copper", "Copper", "Copper", "Copper")
        self.plr.piles[Piles.DISCARD].set("Copper", "Copper", "Copper")
        score = self.plr.get_score_details()
        self.assertEqual(score["Gardens"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

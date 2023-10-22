#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Groundskeeper(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.EMPIRES
        self.desc = "+1 Card. +1 Action. While this is in play, when you gain a Victory card, +1VP"
        self.name = "Groundskeeper"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def hook_gain_card(self, game, player, card):
        if card.isVictory():
            player.add_score("Groundskeeper", 1)
            player.output("Scored 1 from Groundskeeper")
        return {}


###############################################################################
class TestGroundskeeper(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1, initcards=["Groundskeeper"], badcards=["Duchess"]
        )
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Groundskeeper")

    def test_play(self):
        """Play a Groundskeeper"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)
        self.plr.coins.set(5)
        self.plr.buy_card("Duchy")
        self.assertEqual(self.plr.score["Groundskeeper"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Ranger(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+1 Buy. Turn your journey over. If its face up +5 Cards"
        self.name = "Ranger"
        self.buys = 1
        self.cost = 4

    def special(self, game, player):
        """Turn your Journey token over. If it's face up, +5 cards"""
        if player.flip_journey_token():
            player.output("Ranger gives +5 Cards")
            player.pickup_cards(5)


###############################################################################
class Test_Ranger(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Ranger"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Ranger")

    def test_play_first(self):
        """Play a ranger"""
        self.plr.journey_token = True
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 0)
        self.assertFalse(self.plr.journey_token)

    def test_play_second(self):
        """Play a ranger the second time"""
        self.plr.journey_token = False
        self.plr.piles[Piles.HAND].set()
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)
        self.assertTrue(self.plr.journey_token)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

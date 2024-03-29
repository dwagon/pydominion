#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fishingvillage(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.base = Card.CardExpansion.SEASIDE
        self.desc = "+1 coin, +2 actions; next turn +1 coin, +1 action"
        self.name = "Fishing Village"
        self.coin = 1
        self.actions = 2
        self.cost = 3

    def duration(self, game, player):
        """+1 action, +1 coin"""
        player.coins.add(1)
        player.add_actions(1)


###############################################################################
class Test_Fishingvillage(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Fishing Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Fishing Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a fishing village"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.piles[Piles.DURATION].size(), 0)
        self.assertEqual(self.plr.piles[Piles.PLAYED].size(), 1)
        self.assertEqual(self.plr.piles[Piles.PLAYED][-1].name, "Fishing Village")
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

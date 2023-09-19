#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_City(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = """+1 card, +2 action; If there are one or more empty Supply
            piles, +1 card. If there are two or more, +1 coin, +1 buy """
        self.name = "City"
        self.cost = 5
        self.cards = 1
        self.actions = 2

    ###########################################################################
    def special(self, game, player):
        empties = sum([1 for st in game.card_piles if game[st].is_empty()])
        if empties >= 1:
            player.pickup_card()
        if empties >= 2:
            player.coins.add(1)
            player.buys.add(1)


###############################################################################
class TestCity(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["City", "Moat", "Cellar"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.city = self.g["City"].remove()
        self.plr.add_card(self.city, Piles.HAND)

    def test_no_stacks(self):
        """Play a city with no stacks empty"""
        self.plr.play_card(self.city)
        self.g.print_state()
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_one_stack(self):
        """Play a city with one stacks empty"""
        while True:
            c = self.g["Moat"].remove()
            if not c:
                break
        self.plr.play_card(self.city)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)

    def test_two_stack(self):
        """Play a city with two stacks empty"""
        while True:
            c = self.g["Moat"].remove()
            if not c:
                break
        while True:
            c = self.g["Cellar"].remove()
            if not c:
                break
        self.plr.play_card(self.city)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.coins.get(), 1)
        # 1 default + 1 for city
        self.assertEqual(self.plr.buys.get(), 2)
        # 5 for hand, 1 for city, 1 for one stack
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 7)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

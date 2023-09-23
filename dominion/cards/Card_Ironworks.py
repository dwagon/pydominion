#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Ironworks(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.INTRIGUE
        self.desc = "Gain a card costing up to 4. If it is an ... Action card, +1 Action; Treasure card, +1 Coin; Victory card, +1 Card"
        self.name = "Iron Works"
        self.cost = 4

    def special(self, game, player):
        """Gain a card costing up to 4. If it is an action card:
        +1 action; treasure card +1 coin; victory card, +1 card"""
        c = player.plr_gain_card(4, force=True)
        if c.isVictory():
            player.pickup_card()
        if c.isAction():
            player.add_actions(1)
        if c.isTreasure():
            player.coins.add(1)


###############################################################################
class Test_Ironworks(unittest.TestCase):
    def setUp(self):
        # Make most of the cards too expensive to ensure we can select what we want
        initcards = [
            "Iron Works",
            "Mill",
            "Apprentice",
            "Bandit Camp",
            "City",
            "Count",
            "Duke",
            "Library",
            "Market",
            "Rebuild",
        ]
        self.g = Game.TestGame(numplayers=1, initcards=initcards)
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Iron Works")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play_great_hall(self):
        """Use Ironworks to gain a Great Hall"""
        self.plr.test_input = ["Mill"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Mill")
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)

    def test_play_silver(self):
        """Use Ironworks to gain a Silver"""
        self.plr.test_input = ["Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Silver")
        self.assertEqual(self.plr.actions.get(), 0)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)

    def test_play_ironworks(self):
        """Use Ironworks to gain an Ironworks"""
        self.plr.test_input = ["iron"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.DISCARD][-1].name, "Iron Works")
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 0)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

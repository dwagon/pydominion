#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Quarry(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 Coin. While this is in play, Action cards cost 2 less, but not less than 0."
        self.name = "Quarry"
        self.coin = 1
        self.cost = 4

    def hook_card_cost(self, game, player, card):
        if self in player.piles[Piles.PLAYED] and card.isAction():
            return -2
        return 0


###############################################################################
class Test_Quarry(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Quarry", "Moat"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Quarry"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_playcard(self):
        """Play a quarry"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.card_cost(self.g["Gold"]), 6)
        self.assertEqual(self.plr.card_cost(self.g["Moat"]), 0)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()


# EOF

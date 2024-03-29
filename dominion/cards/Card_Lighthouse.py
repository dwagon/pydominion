#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Lighthouse(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.DURATION]
        self.desc = """+1 Action. Now and at the start of your next turn: +1 Coin.
        While this is in play, when another player plays an Attack card, it doesn't affect you."""
        self.name = "Lighthouse"
        self.base = Card.CardExpansion.SEASIDE
        self.defense = True
        self.actions = 1
        self.cost = 2

    def duration(self, game, player):
        player.coins.add(1)

    def special(self, game, player):
        player.coins.add(1)


###############################################################################
class Test_Lighthouse(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Lighthouse"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Lighthouse")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.coins.get(), 1)
        self.plr.end_turn()
        self.plr.start_turn()
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

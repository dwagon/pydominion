#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Highway"""
import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Highway(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = "+1 Card +1 Action. This turn, cards cost $1 less."
        self.name = "Highway"
        self.cards = 1
        self.actions = 1
        self.cost = 5

    def hook_card_cost(self, game, player, card):
        if self in player.piles[Piles.PLAYED]:
            return -1
        return 0


###############################################################################
class TestHighway(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Highway"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Highway")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)
        self.assertEqual(self.plr.actions.get(), 1)

    def test_cost_reduction(self):
        self.coin = 1
        gold = self.g.get_card_from_pile("Gold")
        self.assertEqual(self.plr.card_cost(gold), 6)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.card_cost(gold), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

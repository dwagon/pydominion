#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Princess(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.PRIZE]
        self.base = Card.CardExpansion.CORNUCOPIA
        self.name = "Princess"
        self.purchasable = False
        self.cost = 0
        self.desc = (
            "+1 Buy; While this is in play, cards cost 2 less, but not less than 0."
        )
        self.buys = 1

    def hook_card_cost(self, game, player, card):
        return -2


###############################################################################
class TestPrincess(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Tournament"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Princess")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 2)
        gold = self.g.get_card_from_pile("Gold")
        self.assertEqual(self.plr.card_cost(gold), 4)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

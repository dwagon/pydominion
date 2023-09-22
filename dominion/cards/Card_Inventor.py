#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Inventor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = "Gain a card costing up to 4, then cards cost 1 less this turn (but not less than 0)."
        self.name = "Inventor"
        self.cost = 4

    def special(self, game, player):
        """Gain a card costing up to 4"""
        player.plr_gain_card(4)

    def hook_card_cost(self, game, player, card):
        if self in player.piles[Piles.PLAYED]:
            return -1
        return 0


###############################################################################
class TestInventor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Inventor", "Gardens"],
            badcards=["Blessed Village", "Cemetery"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.inventor = self.g.get_card_from_pile("Inventor")
        self.plr.add_card(self.inventor, Piles.HAND)

    def test_play(self):
        gold = self.g.get_card_from_pile("Gold")
        self.plr.test_input = ["Get Gardens"]
        self.assertEqual(self.plr.card_cost(gold), 6)
        self.plr.play_card(self.inventor)
        self.assertEqual(self.plr.card_cost(gold), 5)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

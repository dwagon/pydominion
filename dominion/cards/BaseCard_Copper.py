#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_Copper(Card.Card):
    """Copper"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.DOMINION
        self.basecard = True
        self.playable = False
        self.callable = False
        self.desc = "+1 coin"
        self.name = "Copper"
        self.coin = 1
        self.cost = 0

    @classmethod
    def calc_numcards(cls, _):
        return 60


###############################################################################
class TestCopper(unittest.TestCase):
    """Test Copper"""

    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1)
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Copper")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Province"""
import unittest

from dominion import Card, Game


###############################################################################
class Card_Province(Card.Card):
    """Province"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.DOMINION
        self.desc = "6 VP"
        self.playable = False
        self.basecard = True
        self.name = "Province"
        self.cost = 8
        self.victory = 6

    @classmethod
    def calc_numcards(cls, game):
        if game.numplayers == 2:
            return 8
        if game.numplayers > 4:
            return 3 * game.numplayers
        return 12


###############################################################################
class TestProvince(unittest.TestCase):
    """Test Province"""

    def test_two_player(self):
        """Two player games"""
        g = Game.TestGame(quiet=True, numplayers=2)
        g.start_game()
        self.assertEqual(len(g.card_piles["Province"]), 8)

    def test_five(self):
        """Five player games"""
        g = Game.TestGame(quiet=True, numplayers=5)
        g.start_game()
        self.assertEqual(len(g.card_piles["Province"]), 15)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

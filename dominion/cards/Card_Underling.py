#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Underling"""
import unittest

from dominion import Game, Piles, Card


###############################################################################
class Card_Underling(Card.Card):
    """Underling"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.LIAISON]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Underling"
        self.cards = 1
        self.actions = 1
        self.favors = 1
        self.desc = "+1 Card; +1 Action; +1 Favor"
        self.cost = 3


###############################################################################
class TestUnderling(unittest.TestCase):
    """Test Underling"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Underling"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Underling")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        favs = self.plr.favors.get()
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.favors.get(), favs + 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 5 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

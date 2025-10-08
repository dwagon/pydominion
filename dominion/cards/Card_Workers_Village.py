#!/usr/bin/env python
"""https://wiki.dominionstrategy.com/index.php/Worker%27s_Village"""
import unittest

from dominion import Game, Card, Piles


###############################################################################
class Card_WorkersVillage(Card.Card):
    """Worker's Village"""

    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.PROSPERITY
        self.desc = "+1 card, +2 actions, +1 buy"
        self.name = "Worker's Village"
        self.cost = 4
        self.cards = 1
        self.actions = 2
        self.buys = 1


###############################################################################
class TestWorkersVillage(unittest.TestCase):
    """Test Worker's Village"""

    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Worker's Village"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Worker's Village")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play Workers Village"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.actions.get(), 2)
        self.assertEqual(self.plr.buys.get(), 2)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

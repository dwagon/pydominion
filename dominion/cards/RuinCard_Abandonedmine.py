#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Abandoned_Mine """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_AbandonedMine(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Abandoned Mine"
        self.purchasable = False
        self.cost = 0
        self.desc = "+1 coin"
        self.coin = 1
        self.pile = "Ruins"


###############################################################################
class TestAbandonedMine(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Ruins", "Abandoned Mine")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play an abandoned mine"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

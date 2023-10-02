#!/usr/bin/env python
""" https://wiki.dominionstrategy.com/index.php/Ruined_Market """

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_RuinedMarket(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.RUIN]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Ruined Market"
        self.desc = "+1 Buy"
        self.purchasable = False
        self.cost = 0
        self.buys = 1
        self.pile = "Ruins"


###############################################################################
class TestRuinedMarket(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=4, initcards=["Cultist"])
        self.g.start_game()
        self.g.print_state()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Ruins", "Ruined Market")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a ruined market"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.buys.get(), 1 + 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

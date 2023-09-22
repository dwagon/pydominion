#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Treasure_Trove(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.ADVENTURE
        self.desc = "+2 Coin. When you play this, gain a Gold and a Copper"
        self.name = "Treasure Trove"
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        """When you play this, gain a Gold and a Copper"""
        player.gain_card("Copper")
        player.gain_card("Gold")
        player.output("Gained a Copper and a Gold")


###############################################################################
class Test_Treasure_Trove(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Treasure Trove"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Treasure Trove")

    def test_play(self):
        """Play a treasure trove"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Copper", self.plr.piles[Piles.DISCARD])
        self.assertIn("Gold", self.plr.piles[Piles.DISCARD])
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_LuckyCoin(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.HEIRLOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "1 Coin; When you play this, gain a Silver."
        self.name = "Lucky Coin"
        self.cost = 4
        self.coin = 1
        self.purchasable = False

    def special(self, game, player):
        player.gain_card("Silver")


###############################################################################
class Test_LuckyCoin(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Fool"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Lucky Coin"].remove()

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.piles[Piles.DISCARD][0].name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

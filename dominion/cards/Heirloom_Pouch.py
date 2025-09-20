#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles


###############################################################################
class Card_Pouch(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.TREASURE, Card.CardType.HEIRLOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+1 Coin, +1 Buy"
        self.name = "Pouch"
        self.cost = 2
        self.coin = 1
        self.buys = 1
        self.purchasable = False


###############################################################################
class Test_Pouch(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Tracker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Pouch")

    def test_play(self):
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.buys.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)
        self.assertEqual(self.plr.buys.get(), 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

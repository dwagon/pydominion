#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Bard(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "+2 Coin; Receive a boon"
        self.name = "Bard"
        self.coin = 2
        self.cost = 4

    def special(self, game, player):
        player.receive_boon()


###############################################################################
class Test_Bard(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.bard = self.g.get_card_from_pile("Bard")
        for b in self.g.boons[:]:
            if b.name == "The Mountain's Gift":
                self.g.boons = [b]
                break

    def test_play_card(self):
        """Play Bard"""
        self.plr.add_card(self.bard, Piles.HAND)
        self.plr.play_card(self.bard)
        self.assertGreaterEqual(self.plr.coins.get(), 2)
        # Check boon happened
        self.assertIn("Silver", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

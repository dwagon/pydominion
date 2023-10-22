#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Baker(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.GUILDS
        self.desc = "+1 card, +1 action, +1 coffer"
        self.name = "Baker"
        self.actions = 1
        self.cards = 1
        self.cost = 5

    def special(self, game, player):
        """Take a Coin Token"""
        player.coffers.add(1)

    def setup(self, game):
        """Each Player takes a coin token"""
        for plr in game.player_list():
            plr.coffers.add(1)


###############################################################################
class Test_Baker(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Baker"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Baker")
        self.plr.add_card(self.card, Piles.HAND)

    def test_setup(self):
        """Test each player having a coin"""
        self.assertEqual(self.plr.coffers.get(), 1)

    def test_play(self):
        """Play a baker"""
        self.plr.coffers.set(0)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coffers.get(), 1)
        self.assertEqual(self.plr.actions.get(), 1)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

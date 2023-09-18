#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Spoils(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.TREASURE
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "+3 coin. When you play this, return it to the Spoils pile."
        self.basecard = True
        self.purchasable = False
        self.name = "Spoils"
        self.cost = 0
        self.coin = 3
        self.numcards = 15

    def special(self, game, player):
        """When you play this return it to the spoils pile"""
        game["Spoils"].add(self)
        player.remove_card(self)


###############################################################################
class TestSpoils(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bandit Camp"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_play(self):
        num_spoils = len(self.g["Spoils"])
        spoils = self.g["Spoils"].remove()
        self.plr.add_card(spoils, Piles.HAND)
        self.plr.play_card(spoils)
        self.assertEqual(self.plr.coins.get(), 3)
        self.assertTrue(self.plr.piles[Piles.PLAYED].is_empty())
        self.assertEqual(len(self.g["Spoils"]), num_spoils)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

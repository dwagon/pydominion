#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Fool(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.FATE]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "If you aren't the player with Lost in the Woods, take it, take 3 Boons, and receive the Boons in any order."
        self.name = "Fool"
        self.cost = 3
        self.heirloom = "Lucky Coin"

    def special(self, game, player):
        if player.has_state("Lost in the Woods"):
            return
        player.assign_state("Lost in the Woods")
        for _ in range(3):
            if not hasattr(player, "_fool_dont_boon"):
                player.receive_boon()
            else:
                player._fool_dont_boon = True


###############################################################################
class Test_Fool(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Fool"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Fool")

    def test_play_with(self):
        """Play a Fool with Lost in the Woods"""
        self.plr.assign_state("Lost in the Woods")
        self.plr._fool_dont_boon = False
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertFalse(self.plr._fool_dont_boon)

    def test_play_without(self):
        """Play a Fool without Lost in the Woods"""
        self.plr._fool_dont_boon = False
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertTrue(self.plr._fool_dont_boon)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

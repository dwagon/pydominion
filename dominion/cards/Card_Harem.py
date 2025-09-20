#!/usr/bin/env python

import unittest

from dominion import Card, Game, Piles, Player


###############################################################################
class Card_Harem(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.VICTORY]
        self.base = Card.CardExpansion.INTRIGUE
        self.name = "Harem"
        self.coin = 2
        self.victory = 2
        self.cost = 6

    def dynamic_description(self, player):
        if player.phase == Player.Phase.BUY:
            return "+2 coin; 2 VPs"
        return "+2 coin"


###############################################################################
class Test_Harem(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Harem"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Harem")
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play a Harem"""
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)

    def test_score(self):
        """Score the harem"""
        sc = self.plr.get_score_details()
        self.assertEqual(sc["Harem"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

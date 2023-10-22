#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Feodum(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "1VP / 3 silvers - trash for 3 silvers"
        self.name = "Feodum"
        self.playable = False
        self.cost = 4

    def special_score(self, game, player):
        """Worth 1VP for every 3 silvers cards in your deck rounded down"""
        numsilver = 0
        for c in player.all_cards():
            if c.name == "Silver":
                numsilver += 1
        return int(numsilver / 3)

    def hook_trash_this_card(self, game, player):
        """When you trash this gain 3 silvers"""
        for _ in range(3):
            player.gain_card("Silver")


###############################################################################
class Test_Feodum(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Feodum"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]

    def test_scoreOne(self):
        self.plr.piles[Piles.HAND].set("Feodum")
        self.plr.piles[Piles.DECK].set("Copper")
        self.plr.piles[Piles.DISCARD].set("Silver", "Silver", "Silver", "Silver")
        self.assertEqual(self.plr.get_score_details()["Feodum"], 1)

    def test_scoreTwo(self):
        self.plr.piles[Piles.HAND].set("Feodum")
        self.plr.piles[Piles.DECK].set("Feodum")
        self.plr.piles[Piles.DISCARD].set(
            "Silver", "Silver", "Silver", "Silver", "Silver", "Silver"
        )
        self.assertEqual(self.plr.get_score_details()["Feodum"], 4)

    def test_trash(self):
        """Trash a Feodum card"""
        card = self.g.get_card_from_pile("Feodum")
        self.plr.add_card(card, Piles.HAND)
        self.plr.trash_card(card)
        self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 3)
        for c in self.plr.piles[Piles.DISCARD]:
            self.assertEqual(c.name, "Silver")


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

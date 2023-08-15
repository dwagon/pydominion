#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Farmland(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.VICTORY
        self.base = Card.CardExpansion.HINTERLANDS
        self.desc = """2VP; When you buy this, trash a card from your hand.
            Gain a card costing exactly 2 more than the trashed card."""
        self.name = "Farmland"
        self.cost = 6
        self.victory = 2

    def hook_gain_this_card(self, game, player):
        c = player.plr_trash_card(force=True)
        player.plr_gain_card(cost=c[0].cost + 2, modifier="equal")
        return {}


###############################################################################
class Test_Farmland(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(
            numplayers=1,
            initcards=["Farmland", "Militia"],
            badcards=["Death Cart", "Cemetery", "Blessed Village"],
        )
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Farmland"].remove()

    def test_gain(self):
        """Gain a farmland"""
        try:
            tsize = self.g.trashpile.size()
            self.plr.piles[Piles.HAND].set("Estate", "Duchy")
            self.plr.test_input = ["Trash Estate", "Get Militia"]
            self.plr.gain_card("Farmland")
            self.assertEqual(self.g.trashpile.size(), tsize + 1)
            self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
            # 1 for farmland, 1 for gained card
            self.assertEqual(self.plr.piles[Piles.DISCARD].size(), 2)
        except (AssertionError, IOError):  # pragma: no cover
            self.g.print_state()
            raise

    def test_score(self):
        self.plr.piles[Piles.DECK].set("Farmland")
        sd = self.plr.get_score_details()
        self.assertEqual(sd["Farmland"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

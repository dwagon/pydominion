#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles


###############################################################################
class Card_Chapel(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.DOMINION
        self.desc = "Trash up to 4 cards"
        self.name = "Chapel"
        self.cost = 2

    def special(self, game, player):
        """Trash up to 4 cards from your hand"""
        player.plr_trash_card(num=4, prompt="Trash up to four cards")


###############################################################################
class Test_Chapel(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Chapel"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.ccard = self.g["Chapel"].remove()
        self.plr.piles[Piles.HAND].set("Copper", "Silver", "Estate")
        self.plr.add_card(self.ccard, Piles.HAND)

    def test_trashnone(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["finish"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 3)
        self.assertEqual(self.g.trash_pile.size(), tsize)

    def test_trashtwo(self):
        tsize = self.g.trash_pile.size()
        self.plr.test_input = ["trash copper", "trash silver", "finish"]
        self.plr.play_card(self.ccard)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 1)
        self.assertEqual(self.g.trash_pile.size(), tsize + 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

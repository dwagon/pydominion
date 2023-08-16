#!/usr/bin/env python

import unittest
from dominion import Boon
from dominion import Card
from dominion import Game, Piles


###############################################################################
class Boon_Flames_Gift(Boon.Boon):
    def __init__(self):
        Boon.Boon.__init__(self)
        self.cardtype = Card.CardType.BOON
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "You may trash a card from your hand"
        self.name = "The Flame's Gift"
        self.purchasable = False

    def special(self, game, player):
        player.plr_trash_card()


###############################################################################
class Test_Flames_Gift(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Bard"], badcards=["Druid"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        for b in self.g.boons:
            if b.name == "The Flame's Gift":
                myboon = b
                break
        self.g.boons = [myboon]
        self.card = self.g["Bard"].remove()

    def test_flames_gift(self):
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.card)
        self.assertIn("Duchy", self.g.trashpile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

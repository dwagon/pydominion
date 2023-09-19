#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.Player import Phase


###############################################################################
class Card_Bat(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Trash up to 2 cards from your hand. If you trashed at least one, exchange this for a Vampire."
        self.name = "Bat"
        self.cost = 2
        self.insupply = False
        self.purchasable = False

    def night(self, game, player):
        tr = player.plr_trash_card(num=2)
        if tr:
            player.replace_card(self, "Vampire")


###############################################################################
class TestBat(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Vampire"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Bat")

    def test_play(self):
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.HAND].set("Duchy", "Silver", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Silver", "Trash Gold", "Finish"]
        self.plr.play_card(self.card)
        self.assertNotIn("Bat", self.plr.piles[Piles.DISCARD])
        self.assertIn("Vampire", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

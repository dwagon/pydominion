#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Recruiter(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.ACTION
        self.base = Card.CardExpansion.RENAISSANCE
        self.desc = """+2 Cards; Trash a card from your hand. +1 Villager per coin it costs."""
        self.name = "Recruiter"
        self.cards = 2
        self.cost = 5

    ###########################################################################
    def special(self, game, player):
        cards = player.plr_trash_card(force=True, num=1)
        player.villagers.add(cards[0].cost)


###############################################################################
class Test_Recruiter(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Recruiter"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g.get_card_from_pile("Recruiter")

    def test_play(self):
        self.plr.piles[Piles.HAND].set("Copper", "Silver")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["Trash Silver"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.piles[Piles.HAND].size(), 2 + 1)
        self.assertEqual(self.plr.villagers.get(), 3)
        self.assertIn("Silver", self.g.trash_pile)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

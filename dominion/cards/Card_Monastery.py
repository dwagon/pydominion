#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card
from dominion.Player import Phase


###############################################################################
class Card_Monastery(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.CardType.NIGHT
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "For each card you've gained this turn, you may trash a card from your hand or a Copper you have in play."
        self.name = "Monastery"
        self.cost = 2

    def night(self, game, player):
        numgained = len(player.stats["gained"])
        if not numgained:
            return
        selectfrom = player.piles[Piles.HAND] + [_ for _ in player.piles[Piles.PLAYED] if _.name == "Copper"]
        player.plr_trash_card(num=numgained, cardsrc=selectfrom)


###############################################################################
class Test_Monastery(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Monastery"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.monastery = self.g.get_card_from_pile("Monastery")

    def test_play_card(self):
        """Play Monastery"""
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.monastery, Piles.HAND)
        self.plr.gain_card("Silver")
        self.plr.test_input = ["Duchy"]
        self.plr.play_card(self.monastery)
        self.assertIn("Duchy", self.g.trash_pile)

    def test_play_no_gained(self):
        """Play Monastery when you didn't gain a card"""
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.add_card(self.monastery, Piles.HAND)
        self.plr.play_card(self.monastery)

    def test_play_copper(self):
        """Play Monastery when you have a copper"""
        self.plr.phase = Phase.NIGHT
        self.plr.piles[Piles.HAND].set("Duchy")
        self.plr.piles[Piles.PLAYED].set("Copper")
        self.plr.add_card(self.monastery, Piles.HAND)
        self.plr.gain_card("Silver")
        self.plr.test_input = ["Copper"]
        self.plr.play_card(self.monastery)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


class Card_Marauder(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.LOOTER,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = "Gain a Spoils from the Spoils pile. Each other player gains a Ruins."
        self.name = "Marauder"
        self.cost = 4
        self.required_cards = ["Spoils"]

    def special(self, game, player):
        for plr in player.attack_victims():
            plr.output("Gained a ruin from %s's Marauder" % player.name)
            plr.gain_card("Ruins")
        player.gain_card("Spoils")


###############################################################################
class Test_Marauder(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Marauder"])
        self.g.start_game()
        self.plr, self.victim = self.g.player_list()
        self.card = self.g["Marauder"].remove()

    def test_play(self):
        """Play a marauder"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertIn("Spoils", self.plr.piles[Piles.DISCARD])
        self.assertTrue(self.victim.piles[Piles.DISCARD][0].isRuin())


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

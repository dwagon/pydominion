#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
import dominion.Card as Card


###############################################################################
class Card_Tormentor(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.ACTION, Card.CardType.ATTACK, Card.CardType.DOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = """+2 Coin; If you have no other cards in play, gain an Imp
            from its pile. Otherwise, each other player receives the next Hex."""
        self.name = "Tormentor"
        self.required_cards = [("Card", "Imp")]
        self.coin = 2
        self.cost = 5

    def special(self, game, player):
        if player.piles[Piles.PLAYED].size() == 1:  # Include this card
            player.gain_card("Imp")
            player.output("Gained an Imp")
        else:
            for pl in player.attack_victims():
                player.output(f"Hexed {pl.name}")
                pl.output(f"Received a hex from {player.name}'s Tormentor")
                pl.receive_hex()


###############################################################################
class Test_Tormentor(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Tormentor"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g["Tormentor"].remove()
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play_imp(self):
        """Play tormentor with no other cards being played"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 2)
        self.assertIn("Imp", self.plr.piles[Piles.DISCARD])

    def test_play_hex(self):
        """Play tormentor with other cards already being played"""
        self.plr.piles[Piles.PLAYED].set("Tormentor")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertNotIn("Imp", self.plr.piles[Piles.DISCARD])
        self.assertTrue(self.vic.has_state("Deluded"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

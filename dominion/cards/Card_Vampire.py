#!/usr/bin/env python

import unittest

import dominion.Card as Card
from dominion import Game, Piles
from dominion.Player import Phase


###############################################################################
class Card_Vampire(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [Card.CardType.NIGHT, Card.CardType.ATTACK, Card.CardType.DOOM]
        self.base = Card.CardExpansion.NOCTURNE
        self.desc = "Each other player receives the next Hex.  Gain a card costing up to 5 other than a Vampire.  Exchange this for a Bat."
        self.name = "Vampire"
        self.cost = 5
        self.required_cards = [("Card", "Bat")]

    def night(self, game, player):
        for pl in player.attack_victims():
            pl.output(f"{player.name}'s Vampire hexed you")
            pl.receive_hex()
        player.plr_gain_card(5, exclude=["Vampire"])
        player.replace_card(self, "Bat")


###############################################################################
class Test_Vampire(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=2, initcards=["Vampire"], badcards=["Duchess"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Vampire")
        self.plr.add_card(self.card, Piles.HAND)
        for h in self.g.hexes[:]:
            if h.name != "Delusion":
                self.g.discarded_hexes.append(h)
                self.g.hexes.remove(h)

    def test_play(self):
        self.plr.test_input = ["Get Duchy"]
        self.plr.phase = Phase.NIGHT
        self.plr.play_card(self.card)
        self.assertTrue(self.vic.has_state("Deluded"))
        self.assertIn("Duchy", self.plr.piles[Piles.DISCARD])
        self.assertNotIn("Vampire", self.plr.piles[Piles.DISCARD])
        self.assertIn("Bat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

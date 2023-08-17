#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles


###############################################################################
class Card_Importer(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = [
            Card.CardType.DURATION,
            Card.CardType.ACTION,
            Card.CardType.LIAISON,
        ]
        self.base = Card.CardExpansion.ALLIES
        self.name = "Importer"
        self.desc = "At the start of your next turn, gain a card costing up to $5."
        self.cost = 3

    def duration(self, game, player):
        player.plr_gain_card(cost=5)

    def setup(self, game):
        """Each player gets 4 favors"""
        for plr in game.player_list():
            plr.favors.add(4)


###############################################################################
class Test_Importer(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(numplayers=1, initcards=["Importer", "moat"], ally="Plateau Shepherds")
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g["Importer"].remove()
        self.plr.add_card(self.card, Piles.HAND)

    def test_play(self):
        """Play the card"""
        self.assertEqual(self.plr.favors.get(), 1 + 4)  # One for using liaison, 4 for this card
        self.plr.test_input = ["Moat"]
        self.plr.play_card(self.card)
        self.plr.start_turn()
        self.assertIn("Moat", self.plr.piles[Piles.DISCARD])


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

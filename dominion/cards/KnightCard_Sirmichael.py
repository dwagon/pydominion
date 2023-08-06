#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Card
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_Sirmichael(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.KNIGHT,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.name = "Sir Michael"
        self.desc = """Each other player discards down to 3 cards in hand.
        Each other player reveals the top 2 cards of his deck, trashes one of them
        costing from 3 to 6, and discards the rest. If a Knight is trashed by this, trash this card."""
        self.cost = 5

    def special(self, game, player):
        for plr in player.attack_victims():
            plr.plr_discard_down_to(3)
        self.knight_special(game, player)


###############################################################################
class Test_Sir_Michael(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Knights"], badcards=["Pooka", "Fool"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        while True:
            self.card = self.g["Knights"].remove()
            if self.card.name == "Sir Michael":
                break

    def test_score(self):
        """Play the Sir"""
        self.vic.test_input = ["1", "2", "0"]
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)
        self.assertEqual(self.vic.hand.size(), 3)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

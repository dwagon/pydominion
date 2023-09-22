#!/usr/bin/env python

import unittest
from dominion import Game, Piles, Card
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_SirVander(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.ATTACK,
            Card.CardType.KNIGHT,
        ]
        self.base = Card.CardExpansion.DARKAGES
        self.desc = """Each other player reveals the top 2 cards of his deck,
        trashes one of them costing from 3 to 6, and discards the rest.
        If a Knight is trashed by this, trash this card.
        When you trash this, gain a Gold."""
        self.name = "Sir Vander"
        self.cost = 5

    def special(self, game, player):
        self.knight_special(game, player)

    def hook_trashcard(self, game, player):
        player.gain_card("gold")


###############################################################################
class TestSirVander(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Knights"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g.get_card_from_pile("Knights")
            if self.card.name == "Sir Vander":
                break

    def test_score(self):
        """Play the Sir"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

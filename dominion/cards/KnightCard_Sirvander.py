#!/usr/bin/env python

import unittest
from dominion import Game
from dominion import Card
from dominion.cards.Card_Knight import KnightCard


###############################################################################
class Card_Sirvander(KnightCard):
    def __init__(self):
        KnightCard.__init__(self)
        self.cardtype = [Card.TYPE_ACTION, Card.TYPE_ATTACK, Card.TYPE_KNIGHT]
        self.base = Game.DARKAGES
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
class Test_Sir_Vander(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Knight"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Knight"].remove()
            if self.card.name == "Sir Vander":
                break

    def test_score(self):
        """Play the Sir"""
        self.plr.add_card(self.card, "hand")
        self.plr.play_card(self.card)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

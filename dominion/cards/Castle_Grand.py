#!/usr/bin/env python

import unittest
from dominion import Card, Game, Piles, Player
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_GrandCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.CASTLE]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 9
        self.victory = 5
        self.name = "Grand Castle"

    def desc(self, player):
        if player.phase == Player.Phase.BUY:
            return """5VP. When you gain this, reveal your hand. 1VP per Victory card in your hand and/or in play."""
        return "5VP"

    def hook_gain_this_card(self, game, player):
        for card in player.piles[Piles.HAND]:
            player.reveal_card(card)
        victory_points = sum([1 for _ in player.piles[Piles.HAND] if _.isVictory()])
        player.output(f"Gaining {victory_points} VPs from your Victory Cards")
        player.add_score("Grand Castle", victory_points)
        for plr in list(game.players.values()):
            victory_points = sum([1 for card in plr.piles[Piles.DURATION] if card.isVictory()])
            player.output(
                f"Gaining {victory_points} VPs from {plr.name}'s Victory Cards"
            )
            player.add_score("Grand Castle", victory_points)


###############################################################################
class TestGrandCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Castles"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()

    def test_play(self):
        """Play a sprawling castle"""
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Grand Castle":
                break
        self.plr.add_card(self.card, Piles.HAND)
        self.assertEqual(self.plr.get_score_details()["Grand Castle"], 5)

    def test_gain(self):
        """Gain Grand Castle"""
        self.plr.piles[Piles.HAND].set("Duchy", "Province")
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Sprawling Castle":  # One before Grand
                break
        self.plr.gain_card("Castles")
        self.assertEqual(self.plr.get_score_details()["Grand Castle"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

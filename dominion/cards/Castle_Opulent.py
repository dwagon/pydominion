#!/usr/bin/env python

import unittest

from dominion import Game, Card, Piles, Player
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_OpulentCastle(CastleCard):
    def __init__(self) -> None:
        CastleCard.__init__(self)
        self.cardtype = [
            Card.CardType.ACTION,
            Card.CardType.VICTORY,
            Card.CardType.CASTLE,
        ]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 7
        self.desc = (
            """Discard any number of Victory cards. +2 Coin per card discarded. +3VP"""
        )
        self.victory = 3
        self.name = "Opulent Castle"
        self.pile = "Castles"

    def special(self, game: "Game.Game", player: "Player.Player") -> None:
        victory_cards = [c for c in player.piles[Piles.HAND] if c.isVictory()]
        cards = player.plr_discard_cards(
            any_number=True,
            cardsrc=victory_cards,
            prompt="Discard any number of Victory cards. +2 Coin per card discarded",
        )
        if cards is not None:
            player.coins.add(len(cards) * 2)


###############################################################################
class TestOpulentCastle(unittest.TestCase):
    def setUp(self) -> None:
        self.g = Game.TestGame(quiet=True, numplayers=2, initcards=["Castles"])
        self.g.start_game()
        self.plr, self.vic = self.g.player_list()
        self.card = self.g.get_card_from_pile("Castles", "Opulent Castle")

    def test_play(self) -> None:
        """Play a castle"""
        self.plr.piles[Piles.HAND].set("Estate", "Duchy", "Province", "Gold")
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.test_input = ["estate", "duchy", "province", "finish"]
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Opulent Castle"], 3)
        self.assertEqual(self.plr.coins.get(), 6)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

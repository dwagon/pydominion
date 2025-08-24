#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_HumbleCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [
            Card.CardType.TREASURE,
            Card.CardType.VICTORY,
            Card.CardType.CASTLE,
        ]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 3
        self.desc = "+1 Coin; Worth 1VP per Castle you have."
        self.coin = 1
        self.name = "Humble Castle"
        self.pile = "Castles"

    def special_score(self, game, player):
        score = 0
        for card in player.all_cards():
            if card.isCastle():
                score += 1
        return score


###############################################################################
class Test_HumbleCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list()[0]
        self.card = self.g.get_card_from_pile("Castles", "Humble Castle")

    def test_play(self):
        """Play a castle"""
        self.plr.add_card(self.card, Piles.HAND)
        self.plr.play_card(self.card)
        self.assertEqual(self.plr.coins.get(), 1)

    def test_score(self):
        self.plr.add_card(self.card, Piles.DISCARD)
        score = self.plr.get_score_details()
        self.assertEqual(score["Humble Castle"], 1)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

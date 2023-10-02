#!/usr/bin/env python

import unittest
from dominion import Game, Card, Piles
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_KingsCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.CardType.VICTORY, Card.CardType.CASTLE]
        self.base = Card.CardExpansion.EMPIRES
        self.cost = 10
        self.desc = "Worth 2VP per Castle you have."
        self.name = "King's Castle"
        self.pile = "Castles"

    def special_score(self, game, player):
        return sum([2 for card in player.all_cards() if card.isCastle()])


###############################################################################
class Test_KingsCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.TestGame(quiet=True, numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list(0)

    def test_have(self):
        """Have a kings castle"""
        self.card = self.g.get_card_from_pile("Castles", "King's Castle")

        self.plr.add_card(self.card, Piles.HAND)
        self.assertEqual(self.plr.get_score_details()["King's Castle"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

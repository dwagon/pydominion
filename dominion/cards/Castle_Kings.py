#!/usr/bin/env python

import unittest
from dominion import Game, Card
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_KingsCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.TYPE_VICTORY, Card.TYPE_CASTLE]
        self.base = Game.EMPIRES
        self.cost = 10
        self.desc = "Worth 2VP per Castle you have."
        self.name = "King's Castle"

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
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "King's Castle":  # One before Kings
                break
        self.plr.add_card(self.card, "hand")
        self.assertEqual(self.plr.get_score_details()["King's Castle"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

#!/usr/bin/env python

import unittest
from dominion import Game, Card
from dominion.cards.Card_Castles import CastleCard


###############################################################################
class Card_CrumblingCastle(CastleCard):
    def __init__(self):
        CastleCard.__init__(self)
        self.cardtype = [Card.TYPE_VICTORY, Card.TYPE_CASTLE]
        self.base = Game.EMPIRES
        self.cost = 4
        self.desc = "1VP. When you gain or trash this, +1VP and gain a Silver."
        self.victory = 1
        self.name = "Crumbling Castle"

    def hook_gain_this_card(self, game, player):
        player.add_score("Crumbling Castle", 1)
        player.gainCard("Silver")

    def hook_trashThisCard(self, game, player):
        player.add_score("Crumbling Castle", 1)
        player.gainCard("Silver")


###############################################################################
class Test_CrumblingCastle(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Castles"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        while True:
            self.card = self.g["Castles"].remove()
            if self.card.name == "Crumbling Castle":
                break

    def test_play(self):
        """Play a castle"""
        self.plr.add_card(self.card, "hand")
        self.plr.playCard(self.card)
        self.assertEqual(self.plr.get_score_details()["Crumbling Castle"], 1)

    def test_trash(self):
        self.plr.trash_card(self.card)
        self.assertEqual(self.plr.get_score_details()["Crumbling Castle"], 1)
        self.assertIsNotNone(self.plr.in_discard("Silver"))


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF

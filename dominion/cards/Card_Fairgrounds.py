#!/usr/bin/env python

import unittest
import dominion.Game as Game
import dominion.Card as Card


###############################################################################
class Card_Fairgrounds(Card.Card):
    def __init__(self):
        Card.Card.__init__(self)
        self.cardtype = Card.TYPE_VICTORY
        self.base = Game.CORNUCOPIA
        self.desc = "2VP / 5 card types"
        self.name = "Fairgrounds"
        self.playable = False
        self.cost = 6

    def special_score(self, game, player):
        """Worth 2VP for every 5 differently named cards in your deck (round down)"""
        numtypes = {c.name for c in player.allCards()}
        return 2 * int(len(numtypes) / 5)


###############################################################################
class Test_Fairgrounds(unittest.TestCase):
    def setUp(self):
        self.g = Game.Game(quiet=True, numplayers=1, initcards=["Fairgrounds"])
        self.g.start_game()
        self.plr = self.g.player_list(0)
        self.card = self.g["Fairgrounds"].remove()

    def test_zero(self):
        """Fairground for 4 types"""
        self.plr.setHand("Copper", "Estate", "Silver", "Fairgrounds")
        self.plr.setDeck("Copper", "Estate", "Silver", "Fairgrounds")
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc["Fairgrounds"], 0)

    def test_one(self):
        """Fairground for 4 types"""
        self.plr.setDeck("Copper", "Estate", "Silver", "Fairgrounds", "Gold")
        sc = self.plr.getScoreDetails()
        self.assertEqual(sc["Fairgrounds"], 2)


###############################################################################
if __name__ == "__main__":  # pragma: no cover
    unittest.main()

# EOF
